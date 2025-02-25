# Standard library imports
import logging
import os
import shutil
import sys
import uuid
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, Any
import s3fs

# Third-party imports
import geopandas as gpd
import numpy as np
import numcodecs
import pandas as pd
import rioxarray as rxr
import xarray as xr
from osgeo import gdal
from shapely.geometry import Polygon
from tqdm import tqdm
from joblib import Parallel, delayed as joblib_delayed
import zarr
import json

# ODC imports
from odc.geo.geobox import GeoBox, GeoboxTiles
from odc.geo.xr import xr_zeros

# Local imports
from coastal_resilience_utilities.utils.geo import transform_point
from coastal_resilience_utilities.summary_stats.summary_stats import summary_stats2
from rasterops.storage import BaseStorage


# Configure logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger("My Personal")
logger.propagate = True
logger.setLevel(logging.DEBUG)


class IntakeMode(Enum):
    READ = "read"
    CREATE = "create"
    WRITE = "write"
    APPEND = "append"


class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    JOBLIB = "joblib"
    DASK = "dask"
    
    def __getstate__(self):
        return self.value
    
    def __setstate__(self, state):
        self = ExecutionMode(state)


class DataCube:
    
    def __init__(self,
            dx: float,
            epsg: int,
            bounds: tuple[float, float, float, float],
            chunk_size: int,
            storage: BaseStorage,
            varnames: list[str],
            nodata: float = np.nan,
            dtype: str = "<f8",
            n_jobs: int = 1,
            store_active_idxs: bool = True,
        ):
        self.dx = dx 
        self.epsg = epsg
        self.bounds = bounds
        self.chunk_size = chunk_size
        self.storage = storage
        self.varnames = varnames
        self.nodata = nodata
        self.dtype = dtype
        self.store_active_idxs = store_active_idxs
    
    def __post_init__(self):
        from rasterops.storage import StorageEncoder
        self.storage.save_metadata("rasterops_config", json.dumps(self.__dict__, cls=StorageEncoder))
        
    @classmethod
    def from_zarr(cls, path: str):
        from rasterops.storage import StorageDecoder
        prefix = '/'.join(path.replace('s3://', '').split('/')[1:])
        s3 = s3fs.S3FileSystem(
            key=os.getenv("AWS_ACCESS_KEY_ID"),
            secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
            client_kwargs={'endpoint_url': os.getenv("AWS_ENDPOINT_URL")},
            asynchronous=True,
        )
        store = zarr.storage.FsspecStore(
            s3,
            path=prefix
        )
        conf = json.loads(zarr.group(store=store).attrs["rasterops_config"], cls=StorageDecoder)
        
        if "id" in conf:
            del conf["id"]
            
        if "execution_mode" in conf:
            del conf["execution_mode"]
            
        return cls(**conf)
    
    def set_execution_mode(self, execution_mode: ExecutionMode, njobs: int = 1):
        self.execution_mode = execution_mode
        self.n_jobs = njobs
        
    @property
    def crs(self) -> str:
        return f"epsg:{self.epsg}"

    @property
    def geobox(self) -> GeoBox:
        return GeoBox.from_bbox(self.bounds, crs=self.crs, resolution=self.dx)

    @property
    def chunk_shape(self) -> tuple[int, int]:
        return (self.chunk_size, self.chunk_size)

    @property
    def tiles(self) -> GeoboxTiles:
        return GeoboxTiles(self.geobox, self.chunk_shape)

    def tiles_by_bounds(
        self, left: float, bottom: float, right: float, top: float
    ) -> GeoboxTiles:
        """
        Filter tiles to given bounds, and return the tile indexes
        """
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            if not (
                bbox.left < right
                and bbox.right > left
                and bbox.bottom < top
                and bbox.top > bottom
            ):
                continue
            yield idx
            
    def get_idxs(self, var, group=None):
        if group is None:
            return self.storage.root_group.attrs["stored_idxs"][var]
        
        return self.storage.root_group.attrs["stored_idxs"][f"{group}/{var}"]
    
    def tiles_for_da(self, da: xr.DataArray):
        """
        Convenience function to reproject a DataArray
        and get the tiles associated with the bounds
        """

        # Get the bounds in the native CRS
        da_bounds = da.rio.bounds()
        da_bl = transform_point(da_bounds[0], da_bounds[1], da.rio.crs, self.crs)
        da_tr = transform_point(da_bounds[2], da_bounds[3], da.rio.crs, self.crs)

        # Get the tiles that intersect with the data array
        return self.tiles_by_bounds(da_bl.x, da_bl.y, da_tr.x, da_tr.y)

    def get_data_layout(self, varnames: list[str] = []):
        if len(varnames) > 0:
            ds = xr_zeros(
                self.geobox, chunks=self.chunk_shape, dtype="float32"
            ).expand_dims(
                {
                    "var": varnames,
                }
            ).rename({"longitude": "x", "latitude": "y"})
            return xr.full_like(ds, self.nodata).to_dataset("var")

        else:
            ds = xr_zeros(
                self.geobox, chunks=self.chunk_shape, dtype="float32"
            ).rename({"longitude": "x", "latitude": "y"})
            return xr.full_like(ds, self.nodata)

    def create_dataset_schema(
        self, group=None, varnames=None, mode: IntakeMode = IntakeMode.CREATE
    ) -> None:
        """
        Initialize a datacube, that has a very simple schema;
        Each array is 2D, and dataarrays within the cube are created for each layer
        """
        varnames_to_create = varnames if varnames else self.varnames

        # Standard 2D schema, could be made more flexible
        big_ds = self.get_data_layout(varnames_to_create)

        if mode == IntakeMode.CREATE:
            big_ds.to_zarr(
                self.storage.get_storage(),
                group=group,
                mode="w",
                compute=False
            )

        elif mode == IntakeMode.APPEND:
            big_ds.to_zarr(
                self.storage.get_storage(),
                group=group,
                mode="a",
                compute=False,
            )

    def get_extents(self) -> None:
        """ """
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            extent = bbox.left, bbox.right, bbox.bottom, bbox.top
            yield idx, extent

    def get_covering_polygons(
        self, idxs: list[tuple[int, int]] = []
    ) -> gpd.GeoDataFrame:
        idxs = [tuple(i) for i in idxs]
        buff = []
        x = []
        y = []
        for idx, extent in self.get_extents():
            if len(idxs) > 0 and idx not in idxs:
                continue

            buff.append(
                Polygon(
                    [
                        (extent[0], extent[2]),
                        (extent[1], extent[2]),
                        (extent[1], extent[3]),
                        (extent[0], extent[3]),
                    ]
                )
            )
            x.append(idx[0])
            y.append(idx[1])

        return gpd.GeoDataFrame(
            pd.DataFrame({"x": x, "y": y}), geometry=buff, crs="EPSG:4326"
        )

    def geobox_to_rxr(self, geobox: GeoBox) -> xr.DataArray:
        # Create a dummy data array with the same shape as the Geobox
        data = np.zeros((geobox.height, geobox.width))
        data_array = xr.DataArray(data, dims=("y", "x"))
        data_array.rio.write_crs(self.crs, inplace=True)
        data_array.rio.write_transform(geobox.transform, inplace=True)

        # Set the x and y coordinates based on the Geobox
        x_coords = (
            np.arange(geobox.width) * geobox.resolution.x
            + geobox.transform.c
            + self.dx / 2.0
        )
        y_coords = (
            np.arange(geobox.height) * geobox.resolution.y
            + geobox.transform.f
            - self.dx / 2.0
        )
        data_array = data_array.assign_coords({"x": x_coords, "y": y_coords})
        data_array = data_array.rio.set_spatial_dims(x_dim="x", y_dim="y")
        data_array.rio.write_nodata(self.nodata, inplace=True)
        # Create a dataset from the data array
        return data_array

    def set_data(
        self,
        var: str,
        idx: tuple[int, int],
        ds: xr.DataArray,
        group: str = None,
        store_idxs: bool = False,
    ):
        src = self.storage.get_group(group)[var]
        if ds.y[0] < ds.y[-1]:
            ds = ds.reindex(y=ds.y[::-1])

        xy_slice = self.get_xy_slice(ds.shape, idx)
        src[xy_slice] = ds.data.astype("float32")
        return idx

    def get_xy_slice(
        self, shape: tuple[int, int], idx: tuple[int, int]
    ) -> tuple[slice, slice]:
        to_return = (
            slice(idx[0] * self.chunk_size, idx[0] * self.chunk_size + shape[0]),
            slice(idx[1] * self.chunk_size, idx[1] * self.chunk_size + shape[1]),
        )
        return to_return

    def intake_data(
        self,
        da: xr.DataArray | xr.Dataset,
        var: str,
        group: str = None,
        only_idxs: list[tuple[int, int]] = [],
        boxbuff: int = 0.1,
        intake_mode: IntakeMode = IntakeMode.APPEND,
        handle_nodata: bool = True,
    ) -> None:
        # Record initial CRS
        init_crs = da.rio.crs
        logging.info(f"Initial CRS: {init_crs}")

        # Handle NoData values
        if handle_nodata:
            try:
                da = da.where(da != da.rio.nodata, self.nodata)
            except Exception as e:
                logging.warning(f"Error handling NoData values: {e}")
                da = da.where(da != da.attrs["_FillValue"], self.nodata)
        logging.info(f"Setting nodata to {self.nodata}")
        da.rio.write_nodata(self.nodata, inplace=True)
        logging.info(f"Setting crs to {init_crs}")
        da.rio.write_crs(init_crs, inplace=True)

        if intake_mode == IntakeMode.CREATE:
            self.create_dataset_schema(group=group)

        elif intake_mode == IntakeMode.APPEND:
            try:
                self.storage.get_group(group)
            except KeyError:
                self.create_dataset_schema(group=group)

        def prep_single_tile(idx: tuple[int, int], da: xr.DataArray):
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            bl = transform_point(bbox.left, bbox.bottom, self.crs, da.rio.crs)
            tr = transform_point(bbox.right, bbox.top, self.crs, da.rio.crs)

            # Get a dummy data array with the same shape as the tile
            empty_tile_as_da = self.geobox_to_rxr(tile)

            # Clip the data array to the tile in the native CRS of the data array
            # Need to buffer a little bit to avoid edge effects after reprojecting
            # boxbuff = 10000
            try:
                da_clipped = da.rio.clip_box(
                    minx=bl.x - boxbuff,
                    miny=bl.y - boxbuff,
                    maxx=tr.x + boxbuff,
                    maxy=tr.y + boxbuff,
                )
                # Now that data is smaller, reproject it to the tile
                da_tiled = da_clipped.rio.reproject_match(empty_tile_as_da)
                return (idx, da_tiled)
            except (rxr.exceptions.NoDataInBounds, rxr.exceptions.OneDimensionalRaster):
                return None

        # Get the tiles that intersect with the data array
        idxs = self.tiles_for_da(da)

        def f(idx):
            for logger_name in ["botocore", "aiobotocore", "s3fs"]:
                logger = logging.getLogger(logger_name)
                logger.setLevel(logging.WARNING)
                logger.propagate = False
            i = prep_single_tile(idx, da)
            if i:
                idx, da_clipped = i
                if np.isnan(da_clipped).all():
                    return
                else:
                    return self.set_data(var, idx, da_clipped, group=group)

        if len(only_idxs) > 0:
            idxs = only_idxs
        else:
            idxs = [i for i in idxs]

        idxs = self._execute_parallel(f, idxs)
        if self.store_active_idxs:
            self._store_active_idxs(idxs, group, var)

    def get_single_xarray_tile(
        self, var: str, idx: tuple[int, int], group: str = None
    ) -> xr.DataArray:
        src = self.storage.get_group(group)[var]
        tile = self.tiles[tuple(idx)]
        da = self.geobox_to_rxr(tile)
        xy_slice = self.get_xy_slice(da.shape, idx)
        data = src[xy_slice]
        # data[data == 0.0] = self.nodata # TODO: This is a hack to handle the fact that the nodata value is 0.0
        da.data = data
        da.rio.write_nodata(self.nodata, inplace=True)
        da.rio.write_crs(self.epsg, inplace=True)
        return da

    def get_xarray_tiles(
        self,
        var: str,
        filter_nan: bool = True,
        get_idxs: list[tuple[int, int]] = [],
        group: str = None,
    ) -> list[xr.DataArray]:
        if len(get_idxs) > 0:
            print("filtering idxs")
            all_tiles = get_idxs
        else:
            all_tiles = [i for i in self.tiles._all_tiles()]

        def process(idx):
            da = self.get_single_xarray_tile(var, idx, group)
            tile = self.tiles[tuple(idx)]

            if filter_nan:
                if np.isnan(da).all():
                    return
                if np.nanmin(da) == self.nodata and np.nanmax(da) == self.nodata:
                    return
                if np.all(da == np.nan):
                    return

            return da, idx, tile

        to_return = self._execute_parallel(process, all_tiles)

        return [i for i in to_return if i is not None]

    def apply_function(
        self,
        f: Callable,
        idxs: list[tuple[int, int]],
        output: str = None,
        args: list = [],
        kwargs: dict = dict(),
        tile_kwargs: dict = dict(),
        group: str = None,
    ):
        def process(idx):
            try:
                _args = []
                for arg in args:
                    if isinstance(arg, XArrayAccessor):
                        try:
                            _args.append(arg.get_xarray_tiles(**tile_kwargs)(idx))
                        except IndexError:
                            return None

                _kwargs = kwargs.copy()
                for key, value in _kwargs.items():
                    if isinstance(value, XArrayAccessor):
                        try:
                            _kwargs[key] = value.get_xarray_tiles(**tile_kwargs)(idx)
                        except IndexError:
                            return None

                result = f(*_args, **_kwargs)

                if output is not None:
                    self.set_data(output, idx, result, group)
                    return idx  # Return idx to track progress
                else:
                    return result

            except Exception as e:
                logger.error(f"Error processing tile {idx}: {e}")
                return None

        results = self._execute_parallel(process, idxs)
        
        if self.store_active_idxs and output is not None:
            self._store_active_idxs(results, group, output)
        
        if not output:
            return [r for r in results if r is not None]

    def export_as_tif(
        self,
        var: str,
        output: str,
        group: str = None,
        idxs: list[tuple[int, int]] = [],
        COG=False,
    ) -> None:
        id = str(uuid.uuid4())
        tmp_dir = f"/tmp/{id}"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_vrt = self.export_as_tif_tiles(var, tmp_dir, group=group, idxs=idxs)
        if COG:
            gdal.Translate(
                output,
                tmp_vrt,
                format="COG",
                creationOptions=["COMPRESS=DEFLATE", "BIGTIFF=YES"],
            )
        else:
            gdal.Translate(
                output,
                tmp_vrt,
                format="GTiff",
                creationOptions=["COMPRESS=LZW", "BIGTIFF=YES"],
            )
        return output

    def export_as_tif_tiles(
        self, var: str, output: str, group: str = None, idxs: list[tuple[int, int]] = []
    ) -> None:
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
        
        if len(idxs) == 0:
            if self.store_active_idxs:
                idxs = self.storage.root_group.attrs["stored_idxs"][f"{group}/{var}"]
            else:
                idxs = [i for i in self.tiles._all_tiles()]

        def process_tile(idx):
            da = self.get_single_xarray_tile(var, idx, group=group)
            if da is None:
                return None

            da.rio.write_crs(self.epsg, inplace=True)
            da.rio.write_nodata(self.nodata, inplace=True)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                da.rio.to_raster(
                    f"{output}/{var}_{idx[0]}_{idx[1]}.tif", compress="LZW"
                )
            return idx

        # Use the parallel execution framework
        self._execute_parallel(process_tile, idxs)
        tmp_vrt = gdal.BuildVRT(
            f"{output}/vrt.vrt",
            [os.path.join(output, f) for f in os.listdir(output) if f.endswith(".tif")],
        )
        return tmp_vrt
        

    def as_da(self, var: str, group=None, idxs: list[tuple[int, int]] = []) -> None:
        id = str(uuid.uuid4())
        tmp_file = f"/tmp/{id}.tif"
        self.export_as_tif(var, tmp_file, group=group, idxs=idxs)
        return rxr.open_rasterio(tmp_file)

    def _execute_parallel(
        self,
        func: Callable,
        items: Iterable[Any],
        show_progress: bool = True
    ) -> list:
        """Internal method to handle parallel execution"""
        items = list(items)
        logger.info(
            f"Starting parallel operation with {len(items)} items using {self.execution_mode} mode"
        )
        logger.debug(f"Function to execute: {func.__name__}")

        if self.execution_mode == ExecutionMode.SEQUENTIAL:
            logger.info("Using sequential processing")
            if show_progress:
                return [func(item) for item in tqdm(items)]
            return [func(item) for item in items]

        elif self.execution_mode == ExecutionMode.JOBLIB:
            logger.info(f"Using joblib with {self.n_jobs} workers")
            if show_progress:
                return Parallel(n_jobs=self.n_jobs)(
                    joblib_delayed(func)(item) for item in tqdm(items)
                )
            return Parallel(n_jobs=self.n_jobs)(
                joblib_delayed(func)(item) for item in items
            )

        elif self.execution_mode == ExecutionMode.DASK.value:
            import dask
            from dask.distributed import get_client, progress

            client = get_client()
            logger.info(
                f"Using Dask with {len(client.scheduler_info()['workers'])} workers"
            )

            delayed_func = dask.delayed(func)
            delayed_items = [delayed_func(item) for item in items]
            futures = dask.persist(*delayed_items)
            progress(futures, notebook=False)
            results = dask.compute(*futures)

            return results

        else:
            logger.error(f"Invalid execution mode: {self.execution_mode}")
            raise ValueError(f"Unknown execution mode: {self.execution_mode}")
        
    def _store_active_idxs(self, results, group, output):
        logging.info(f"Processed {len(results)} tiles")
        if "stored_idxs" not in self.storage.root_group.attrs:
            self.storage.root_group.attrs["stored_idxs"] = dict()
        
        results = [i for i in results if i is not None]
        
        if f"{group}/{output}" in self.storage.root_group.attrs["stored_idxs"]:
            results = self.storage.root_group.attrs["stored_idxs"][f"{group}/{output}"] + results
            results = list(set([tuple(i) for i in results]))
        
        self.storage.root_group.attrs["stored_idxs"] = {
            **self.storage.root_group.attrs["stored_idxs"],
            f"{group}/{output}": results
        }


@dataclass(frozen=True)
class XArrayAccessor:
    dc: DataCube
    var: str
    group: str = None

    def get_xarray_tiles(self, **kwargs):

        def f(idx):
            return self.dc.get_single_xarray_tile(self.var, idx, group=self.group)

        return f


def optimize_coord_encoding(values, dx):
    dx_all = np.diff(values)
    np.testing.assert_allclose(dx_all, dx), "must be regularly spaced"

    offset_codec = numcodecs.FixedScaleOffset(
        offset=values[0], scale=1 / dx, dtype=values.dtype, astype="i8"
    )
    delta_codec = numcodecs.Delta("i8", "i2")
    compressor = numcodecs.Blosc(cname="zstd")

    enc0 = offset_codec.encode(values)
    # everything should be offset by 1 at this point
    np.testing.assert_equal(np.unique(np.diff(enc0)), [1])
    enc1 = delta_codec.encode(enc0)
    # now we should be able to compress the shit out of this
    enc2 = compressor.encode(enc1)
    decoded = offset_codec.decode(delta_codec.decode(compressor.decode(enc2)))

    # will produce numerical precision differences
    # np.testing.assert_equal(values, decoded)
    np.testing.assert_allclose(values, decoded)

    return {"compressor": compressor, "filters": (offset_codec, delta_codec)}


def summary_stats(
    dc: DataCube,
    var: str,
    gdf: gpd.GeoDataFrame,
    group: str = None,
    stats=["sum", "count"],
    return_with_fields: bool = False,
):
    logging.info(var)
    tiles = dc.get_xarray_tiles(var, group=group)
    gdf = gdf.reset_index()

    buff = []
    for da, idx, tile in tiles:
        bbox = tile.boundingbox
        extent = bbox.left, bbox.right, bbox.bottom, bbox.top
        _gdf = gdf.cx[extent[0] : extent[1], extent[2] : extent[3]]
        if _gdf.shape[0] == 0:
            continue

        output = summary_stats2(_gdf, da, stats)
        buff.append(output)

    output = (
        pd.concat(buff)
        .groupby(["index", "geometry"])
        .apply(lambda x: x.apply(np.nansum))
        .reset_index()
        .set_index("index")
    )
    # output = pd.concat(buff).groupby(["index", "geometry"]).sum().reset_index().set_index("index")
    if return_with_fields:
        return pd.merge(
            gdf,
            output[[c for c in output.columns if c != "geometry"]],
            left_index=True,
            right_index=True,
            how="left",
        )

    else:
        gdf["dummycolumn"] = 0
        return pd.merge(
            gdf[["dummycolumn"]],
            output[[c for c in output.columns if c != "geometry"]],
            left_index=True,
            right_index=True,
            how="left",
        ).drop(columns=["dummycolumn"])
        # return output

import asyncio
import concurrent
from typing import Callable, List
import gc
from rasterops import datacube2
import xarray as xr
import numpy as np
from tqdm import tqdm


def multi_intake(dc: datacube2.DataCube, group: str, data: dict[str, xr.DataArray]):
    INGESTED = []
    for idx, (var, da) in enumerate(data.items()):
        print(f"Ingesting {var}")
        dc.intake_data(da, var, group=group)
        dc.storage.repo.commit(f"Intake {var}")
        INGESTED.append(var)
        gc.collect()
        
    return INGESTED


def first(da1: xr.DataArray, da2: xr.DataArray):
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning, message="All-NaN axis encountered")
    return da1.copy(data=np.nanmax([da1.data, da2.data], axis=0))


def compile(dc, output, vars, group, resolve_function=first):
    for var in tqdm(vars):
        idxs = dc.storage.root_group.attrs["stored_idxs"][f"{group}/{var}"]
        print(f"{var} -> {output}")
        dc.apply_function(
            resolve_function, 
            idxs, 
            output, 
            kwargs = {
                "da1": datacube2.XArrayAccessor(dc, var=var, group=group),
                "da2": datacube2.XArrayAccessor(dc, var=output, group=group),
            },
            tile_kwargs={"filter_nan": False},
            group=group,
        )
        dc.storage.repo.commit(f"Compile {var}")
    
    dc.storage.repo.commit(f"Compile {var}")
import zarr
from pathlib import Path
import s3fs
import os
import logging
import json
import numpy as np

class BaseStorage:
    def __init__(self):
        pass

    def get_storage(self):
        pass

    def get_root_group(self):
        pass

    def create_dataset(self, shape, group=None, varnames=None):
        pass


class ArrayLakeStorage(BaseStorage):
    def __init__(self, client: str, repo: str, disk_store: str):
        self.client = client
        self.repo = repo
        self.disk_store = disk_store

    def get_storage(self):
        return self.repo.store

    @property
    def root_group(self):
        return self.repo.root_group

    def create_group(self, group: str):
        self.root_group.create_group(group)

    def get_group(self, group: str = None):
        return self.root_group[group]

    def delete_group(self, group: str):
        del self.root_group[group]

    def create_dataset(self, var, group=None, varnames=None):
        pass


class DummyRepo:
    def commit(self, message: str):
        pass


class PlainOlZarrStore(BaseStorage):
    def __init__(self, path: str):
        self.path = path  # Save the path for serialization
        self._initialize_store()
        
    def _initialize_store(self):
        """Initialize the store after basic attributes are set"""
        if self.path.startswith('s3://'):
            # Parse S3 URL
            bucket = self.path.replace('s3://', '').split('/')[0]
            prefix = '/'.join(self.path.replace('s3://', '').split('/')[1:])
            s3 = s3fs.S3FileSystem(
                key=os.getenv("AWS_ACCESS_KEY_ID"),
                secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
                client_kwargs={'endpoint_url': os.getenv("AWS_ENDPOINT_URL")},
                asynchronous=True,
            )
            
            self.store = zarr.storage.FsspecStore(
                s3,
                path=prefix
            )
            
        else:
            # Fallback to local storage
            self.store = zarr.storage.DirectoryStore(Path(self.path) / "data.zarr")
        self.repo = DummyRepo()

    def __getstate__(self):
        """Return state for JSON serialization"""
        return {'path': self.path}

    def __setstate__(self, state):
        """Reconstruct object from JSON serialization"""
        self.path = state['path']
        self._initialize_store()
    
    def save_metadata(self, key: str, values: dict):
        self.root_group.attrs[key] = values

    def get_storage(self):
        return self.store

    @property
    def root_group(self):
        return zarr.group(store=self.store)

    def create_group(self, group: str = ''):
        self.root_group.create_group(group)

    def get_group(self, group: str = None):
        return self.root_group[group]

    def delete_group(self, group: str):
        del self.root_group[group]

    def create_dataset(self, var, group=None, varnames=None):
        pass


class StorageEncoder(json.JSONEncoder):
    def default(self, obj):
        from rasterops.rasterops import ExecutionMode
        if isinstance(obj, PlainOlZarrStore):
            return obj.path
        return super().default(obj)

class StorageDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        from rasterops.rasterops import ExecutionMode
        if "path" in obj:
            return PlainOlZarrStore(obj["path"])
        return obj


# Saving this for when icechunk is production ready
# import icechunk

# class IceChunkLocalDatastore(BaseStorage):

#     def __init__(self, path: str, mode: str = "w"):
#         storage_config = icechunk.StorageConfig.filesystem(path)
#         try:
#             self.store = icechunk.IcechunkStore.create(storage_config, mode=mode)
#         except ValueError:
#             self.store = icechunk.IcechunkStore.open_existing(
#                 storage=storage_config, mode="r+"
#             )

#     def get_storage(self):
#         return self.store

#     @property
#     def root_group(self):
#         return zarr.group(store=self.store)

#     def create_group(self, group: str):
#         self.root_group.create_group(group)

#     def get_group(self, group: str = None):
#         return self.root_group[group]

#     def delete_group(self, group: str):
#         del self.root_group[group]

#     def create_dataset(self, var, group=None, varnames=None):
#         pass


# class IceChunkS3Datastore(BaseStorage):
#     def __init__(
#         self,
#         bucket: str,
#         prefix: str,
#         credentials: icechunk.S3Credentials,
#         endpoint_url: str,
#         allow_http: bool,
#         region: str,
#         mode: str = "w",
#     ):
#         storage_config = icechunk.StorageConfig.s3_from_config(
#             bucket=bucket,
#             prefix=prefix,
#             credentials=credentials,
#             endpoint_url=endpoint_url,
#             allow_http=allow_http,
#             region=region,
#         )
#         try:
#             self.store = icechunk.IcechunkStore.create(storage_config, mode=mode)
#         except ValueError:
#             self.store = icechunk.IcechunkStore.open_existing(
#                 storage=storage_config, mode="r+"
#             )

#     def get_storage(self):
#         return self.store

#     @property
#     def root_group(self):
#         return zarr.group(store=self.store)

#     def create_group(self, group: str):
#         self.root_group.create_group(group)

#     def get_group(self, group: str = None):
#         return self.root_group[group]

#     def delete_group(self, group: str):
#         del self.root_group[group]

#     def create_dataset(self, var, group=None, varnames=None):
#         pass

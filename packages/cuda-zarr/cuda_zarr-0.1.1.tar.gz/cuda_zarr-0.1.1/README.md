# cuda-zarr

A simple `zarr-python` [v3 compatible store](https://zarr.readthedocs.io/en/stable/user-guide/storage.html#developing-custom-stores) that uses the `CuFile` API: https://docs.rapids.ai/api/kvikio/stable/quickstart/
plus (at least one) codec(s).

## install (once on pypi)

```shell
uv pip install cuda-zarr[cuda12]
```

## usage

Nvidia's documentation on how level/checksum are used is quite sparse, but testing seems to show levels 1-22 all work. This codec only seems to work when used either roundtrip i.e., data is read and written using it, or only read. If you write data with this, it seems you can't read it back in with CPU data.

```python
from cuda_zarr import LZ4GPU, CuFileStore
register_codec("zstd", LZ4GPU)
zarr.config.set({'codecs.zstd': f"{LZ4GPU.__module__}.{LZ4GPU.__name__}", "buffer": "zarr.core.buffer.gpu.Buffer", "ndbuffer": "zarr.core.buffer.gpu.NDBuffer"})
store = CuFileStore('/path/to/store')
...
```

Untested in unit testing is the `RemoteCuFileStore` with s3 (although `http` is tested). Also `RemoteCuFileStore` only supports `get` and not `set` via `kvikio` (it will go through normal CPU based `fsspec` `io` in the `set` case).

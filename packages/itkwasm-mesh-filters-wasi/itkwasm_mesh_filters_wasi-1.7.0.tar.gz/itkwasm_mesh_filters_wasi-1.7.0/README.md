# itkwasm-mesh-filters-wasi

[![PyPI version](https://badge.fury.io/py/itkwasm-mesh-filters-wasi.svg)](https://badge.fury.io/py/itkwasm-mesh-filters-wasi)

Mesh filters to repair, remesh, subdivide, decimate, smooth, triangulate, etc. WASI implementation.

This package provides the WASI WebAssembly implementation. It is usually not called directly. Please use [`itkwasm-mesh-filters`](https://pypi.org/project/itkwasm-mesh-filters/) instead.


## Installation

```sh
pip install itkwasm-mesh-filters-wasi
```

## Development

```sh
pip install pytest
pip install -e .
pytest

# or
pip install hatch
hatch run test
```

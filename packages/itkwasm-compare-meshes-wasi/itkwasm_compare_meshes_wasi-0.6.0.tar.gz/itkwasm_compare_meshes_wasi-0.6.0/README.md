# itkwasm-compare-meshes-wasi

[![PyPI version](https://badge.fury.io/py/itkwasm-compare-meshes-wasi.svg)](https://badge.fury.io/py/itkwasm-compare-meshes-wasi)

Compare meshes and polydata for regression testing. WASI implementation.

This package provides the WASI WebAssembly implementation. It is usually not called directly. Please use [`itkwasm-compare-meshes`](https://pypi.org/project/itkwasm-compare-meshes/) instead.


## Installation

```sh
pip install itkwasm-compare-meshes-wasi
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

# itkwasm-mesh-filters-emscripten

[![PyPI version](https://badge.fury.io/py/itkwasm-mesh-filters-emscripten.svg)](https://badge.fury.io/py/itkwasm-mesh-filters-emscripten)

Mesh filters to repair, remesh, subdivide, decimate, smooth, triangulate, etc. Emscripten implementation.

This package provides the Emscripten WebAssembly implementation. It is usually not called directly. Please use the [`itkwasm-mesh-filters`](https://pypi.org/project/itkwasm-mesh-filters/) instead.


## Installation

```sh
import micropip
await micropip.install('itkwasm-mesh-filters-emscripten')
```

## Development

```sh
pip install hatch
hatch run download-pyodide
hatch run test
```

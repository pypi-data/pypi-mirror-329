# itkwasm-compare-meshes-emscripten

[![PyPI version](https://badge.fury.io/py/itkwasm-compare-meshes-emscripten.svg)](https://badge.fury.io/py/itkwasm-compare-meshes-emscripten)

Compare meshes and polydata for regression testing. Emscripten implementation.

This package provides the Emscripten WebAssembly implementation. It is usually not called directly. Please use the [`itkwasm-compare-meshes`](https://pypi.org/project/itkwasm-compare-meshes/) instead.


## Installation

```sh
import micropip
await micropip.install('itkwasm-compare-meshes-emscripten')
```

## Development

```sh
pip install hatch
hatch run download-pyodide
hatch run test
```

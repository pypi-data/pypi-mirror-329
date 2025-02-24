import pytest
import sys

if sys.version_info < (3,10):
    pytest.skip("Skipping pyodide tests on older Python", allow_module_level=True)

from pytest_pyodide import run_in_pyodide

from .fixtures import package_wheel, input_data

@run_in_pyodide(packages=['micropip'])
async def test_compare_meshes_async(selenium, package_wheel):
    import micropip
    await micropip.install(package_wheel)

    from itkwasm_compare_meshes_emscripten import compare_meshes_async

    # Write your test code here

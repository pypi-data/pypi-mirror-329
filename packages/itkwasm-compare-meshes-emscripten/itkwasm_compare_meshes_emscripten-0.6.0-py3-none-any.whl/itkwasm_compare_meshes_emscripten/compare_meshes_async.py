# Generated file. To retain edits, remove this comment.

from pathlib import Path
import os
from typing import Dict, Tuple, Optional, List, Any

from .js_package import js_package

from itkwasm.pyodide import (
    to_js,
    to_py,
    js_resources
)
from itkwasm import (
    InterfaceTypes,
    Mesh,
)

async def compare_meshes_async(
    test_mesh: Mesh,
    baseline_meshes: List[Mesh] = [],
    points_difference_threshold: float = 1e-08,
    number_of_different_points_tolerance: int = 0,
    point_data_difference_threshold: float = 1e-08,
    number_of_point_data_tolerance: int = 0,
    cell_data_difference_threshold: float = 1e-08,
    number_of_cell_data_tolerance: int = 0,
) -> Tuple[Any, Mesh, Mesh, Mesh]:
    """Compare meshes with a tolerance for regression testing.

    :param test_mesh: The input test mesh
    :type  test_mesh: Mesh

    :param baseline_meshes: Baseline images to compare against
    :type  baseline_meshes: Mesh

    :param points_difference_threshold: Difference for point components to be considered different.
    :type  points_difference_threshold: float

    :param number_of_different_points_tolerance: Number of points whose points exceed the difference threshold that can be different before the test fails.
    :type  number_of_different_points_tolerance: int

    :param point_data_difference_threshold: Difference for point data components to be considered different. 
    :type  point_data_difference_threshold: float

    :param number_of_point_data_tolerance: Number of point data that can exceed the difference threshold before the test fails.
    :type  number_of_point_data_tolerance: int

    :param cell_data_difference_threshold: Difference for cell data components to be considered different.
    :type  cell_data_difference_threshold: float

    :param number_of_cell_data_tolerance: Number of cell data that can exceed the difference threshold before the test fails.
    :type  number_of_cell_data_tolerance: int

    :return: Metrics for the closest baseline.
    :rtype:  Any

    :return: Mesh with the differences between the points of the test mesh and the closest baseline.
    :rtype:  Mesh

    :return: Mesh with the differences between the point data of the test mesh and the closest baseline.
    :rtype:  Mesh

    :return: Mesh with the differences between the cell data of the test mesh and the closest baseline.
    :rtype:  Mesh
    """
    js_module = await js_package.js_module
    web_worker = js_resources.web_worker

    kwargs = {}
    if baseline_meshes is not None:
        kwargs["baselineMeshes"] = to_js(baseline_meshes)
    if points_difference_threshold:
        kwargs["pointsDifferenceThreshold"] = to_js(points_difference_threshold)
    if number_of_different_points_tolerance:
        kwargs["numberOfDifferentPointsTolerance"] = to_js(number_of_different_points_tolerance)
    if point_data_difference_threshold:
        kwargs["pointDataDifferenceThreshold"] = to_js(point_data_difference_threshold)
    if number_of_point_data_tolerance:
        kwargs["numberOfPointDataTolerance"] = to_js(number_of_point_data_tolerance)
    if cell_data_difference_threshold:
        kwargs["cellDataDifferenceThreshold"] = to_js(cell_data_difference_threshold)
    if number_of_cell_data_tolerance:
        kwargs["numberOfCellDataTolerance"] = to_js(number_of_cell_data_tolerance)

    outputs = await js_module.compareMeshes(to_js(test_mesh), webWorker=web_worker, noCopy=True, **kwargs)

    output_web_worker = None
    output_list = []
    outputs_object_map = outputs.as_object_map()
    for output_name in outputs.object_keys():
        if output_name == 'webWorker':
            output_web_worker = outputs_object_map[output_name]
        else:
            output_list.append(to_py(outputs_object_map[output_name]))

    js_resources.web_worker = output_web_worker

    if len(output_list) == 1:
        return output_list[0]
    return tuple(output_list)

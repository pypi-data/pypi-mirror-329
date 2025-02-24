# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
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
    func = environment_dispatch("itkwasm_compare_meshes", "compare_meshes_async")
    output = await func(test_mesh, baseline_meshes=baseline_meshes, points_difference_threshold=points_difference_threshold, number_of_different_points_tolerance=number_of_different_points_tolerance, point_data_difference_threshold=point_data_difference_threshold, number_of_point_data_tolerance=number_of_point_data_tolerance, cell_data_difference_threshold=cell_data_difference_threshold, number_of_cell_data_tolerance=number_of_cell_data_tolerance)
    return output

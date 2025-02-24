# Generated file. To retain edits, remove this comment.

from pathlib import Path, PurePosixPath
import os
from typing import Dict, Tuple, Optional, List, Any

from importlib_resources import files as file_resources

_pipeline = None

from itkwasm import (
    InterfaceTypes,
    PipelineOutput,
    PipelineInput,
    Pipeline,
    Mesh,
)

def compare_meshes(
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
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_compare_meshes_wasi').joinpath(Path('wasm_modules') / Path('compare-meshes.wasi.wasm')))

    pipeline_outputs: List[PipelineOutput] = [
        PipelineOutput(InterfaceTypes.JsonCompatible),
        PipelineOutput(InterfaceTypes.Mesh),
        PipelineOutput(InterfaceTypes.Mesh),
        PipelineOutput(InterfaceTypes.Mesh),
    ]

    pipeline_inputs: List[PipelineInput] = [
        PipelineInput(InterfaceTypes.Mesh, test_mesh),
    ]

    args: List[str] = ['--memory-io',]
    # Inputs
    args.append('0')
    # Outputs
    metrics_name = '0'
    args.append(metrics_name)

    points_difference_mesh_name = '1'
    args.append(points_difference_mesh_name)

    point_data_difference_mesh_name = '2'
    args.append(point_data_difference_mesh_name)

    cell_data_difference_mesh_name = '3'
    args.append(cell_data_difference_mesh_name)

    # Options
    input_count = len(pipeline_inputs)
    if len(baseline_meshes) < 1:
       raise ValueError('"baseline-meshes" kwarg must have a length > 1')
    if len(baseline_meshes) > 0:
        args.append('--baseline-meshes')
        for value in baseline_meshes:
            pipeline_inputs.append(PipelineInput(InterfaceTypes.Mesh, value))
            args.append(str(input_count))
            input_count += 1

    if points_difference_threshold:
        args.append('--points-difference-threshold')
        args.append(str(points_difference_threshold))

    if number_of_different_points_tolerance:
        args.append('--number-of-different-points-tolerance')
        args.append(str(number_of_different_points_tolerance))

    if point_data_difference_threshold:
        args.append('--point-data-difference-threshold')
        args.append(str(point_data_difference_threshold))

    if number_of_point_data_tolerance:
        args.append('--number-of-point-data-tolerance')
        args.append(str(number_of_point_data_tolerance))

    if cell_data_difference_threshold:
        args.append('--cell-data-difference-threshold')
        args.append(str(cell_data_difference_threshold))

    if number_of_cell_data_tolerance:
        args.append('--number-of-cell-data-tolerance')
        args.append(str(number_of_cell_data_tolerance))


    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = (
        outputs[0].data,
        outputs[1].data,
        outputs[2].data,
        outputs[3].data,
    )
    return result


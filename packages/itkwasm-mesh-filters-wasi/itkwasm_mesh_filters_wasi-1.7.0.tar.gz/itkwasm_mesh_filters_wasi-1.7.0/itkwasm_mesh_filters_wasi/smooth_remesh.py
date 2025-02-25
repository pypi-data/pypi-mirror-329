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

def smooth_remesh(
    input_mesh: Mesh,
    number_points: float = 75,
    triangle_shape_adaptation: float = 1,
    triangle_size_adaptation: float = 0,
    normal_iterations: int = 3,
    lloyd_iterations: int = 5,
    newton_iterations: int = 30,
    newton_m: int = 7,
    lfs_samples: int = 10000,
) -> Mesh:
    """Smooth and remesh a mesh to improve quality.

    :param input_mesh: The input mesh
    :type  input_mesh: Mesh

    :param number_points: Number of points as a percent of the bounding box diagonal. Output may have slightly more points.
    :type  number_points: float

    :param triangle_shape_adaptation: Triangle shape adaptation factor. Use 0.0 to disable.
    :type  triangle_shape_adaptation: float

    :param triangle_size_adaptation: Triangle size adaptation factor. Use 0.0 to disable.
    :type  triangle_size_adaptation: float

    :param normal_iterations: Number of normal smoothing iterations.
    :type  normal_iterations: int

    :param lloyd_iterations: Number of Lloyd relaxation iterations.
    :type  lloyd_iterations: int

    :param newton_iterations: Number of Newton iterations.
    :type  newton_iterations: int

    :param newton_m: Number of Newton evaluations per step for Hessian approximation.
    :type  newton_m: int

    :param lfs_samples: Number of samples for size adaptation if triangle size adaptation is not 0.0.
    :type  lfs_samples: int

    :return: The output repaired mesh.
    :rtype:  Mesh
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_mesh_filters_wasi').joinpath(Path('wasm_modules') / Path('smooth-remesh.wasi.wasm')))

    pipeline_outputs: List[PipelineOutput] = [
        PipelineOutput(InterfaceTypes.Mesh),
    ]

    pipeline_inputs: List[PipelineInput] = [
        PipelineInput(InterfaceTypes.Mesh, input_mesh),
    ]

    args: List[str] = ['--memory-io',]
    # Inputs
    args.append('0')
    # Outputs
    output_mesh_name = '0'
    args.append(output_mesh_name)

    # Options
    input_count = len(pipeline_inputs)
    if number_points:
        args.append('--number-points')
        args.append(str(number_points))

    if triangle_shape_adaptation:
        args.append('--triangle-shape-adaptation')
        args.append(str(triangle_shape_adaptation))

    if triangle_size_adaptation:
        args.append('--triangle-size-adaptation')
        args.append(str(triangle_size_adaptation))

    if normal_iterations:
        args.append('--normal-iterations')
        args.append(str(normal_iterations))

    if lloyd_iterations:
        args.append('--lloyd-iterations')
        args.append(str(lloyd_iterations))

    if newton_iterations:
        args.append('--newton-iterations')
        args.append(str(newton_iterations))

    if newton_m:
        args.append('--newton-m')
        args.append(str(newton_m))

    if lfs_samples:
        args.append('--lfs-samples')
        args.append(str(lfs_samples))


    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = outputs[0].data
    return result


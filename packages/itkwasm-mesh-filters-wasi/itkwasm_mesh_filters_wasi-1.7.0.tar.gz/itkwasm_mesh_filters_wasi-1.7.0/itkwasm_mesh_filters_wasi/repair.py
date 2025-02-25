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

def repair(
    input_mesh: Mesh,
    merge_tolerance: float = 1e-06,
    minimum_component_area: float = 3,
    maximum_hole_area: float = 0.1,
    maximum_hole_edges: int = 2000,
    maximum_degree3_distance: float = 0,
    remove_intersecting_triangles: bool = False,
) -> Mesh:
    """Repair a mesh so it is 2-manifold and optionally watertight.

    :param input_mesh: The input mesh
    :type  input_mesh: Mesh

    :param merge_tolerance: Point merging tolerance as a percent of the bounding box diagonal.
    :type  merge_tolerance: float

    :param minimum_component_area: Minimum component area as a percent of the total area. Components smaller than this are removed.
    :type  minimum_component_area: float

    :param maximum_hole_area: Maximum area of a hole as a percent of the total area. Holes smaller than this are filled.
    :type  maximum_hole_area: float

    :param maximum_hole_edges: Maximum number of edges in a hole. Holes with fewer edges than this are filled.
    :type  maximum_hole_edges: int

    :param maximum_degree3_distance: Maximum distance as a percent of the bounding box diagonal. Vertices with degree 3 that are closer than this are merged.
    :type  maximum_degree3_distance: float

    :param remove_intersecting_triangles: Remove intersecting triangles.
    :type  remove_intersecting_triangles: bool

    :return: The output repaired mesh.
    :rtype:  Mesh
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_mesh_filters_wasi').joinpath(Path('wasm_modules') / Path('repair.wasi.wasm')))

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
    if merge_tolerance:
        args.append('--merge-tolerance')
        args.append(str(merge_tolerance))

    if minimum_component_area:
        args.append('--minimum-component-area')
        args.append(str(minimum_component_area))

    if maximum_hole_area:
        args.append('--maximum-hole-area')
        args.append(str(maximum_hole_area))

    if maximum_hole_edges:
        args.append('--maximum-hole-edges')
        args.append(str(maximum_hole_edges))

    if maximum_degree3_distance:
        args.append('--maximum-degree3-distance')
        args.append(str(maximum_degree3_distance))

    if remove_intersecting_triangles:
        args.append('--remove-intersecting-triangles')


    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = outputs[0].data
    return result


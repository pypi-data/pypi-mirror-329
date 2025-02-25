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

def slice_mesh(
    input_mesh: Mesh,
    planes: Any,
) -> Mesh:
    """Slice a mesh along planes into polylines.

    :param input_mesh: The input triangle mesh.
    :type  input_mesh: Mesh

    :param planes: An array of plane locations to slice the mesh. Each plane is defined by an array of 'origin' and 'spacing' values.
    :type  planes: Any

    :return: The output mesh comprised of polylines. Cell data indicates whether part of a closed line. Point data indicates the slice index.
    :rtype:  Mesh
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_mesh_filters_wasi').joinpath(Path('wasm_modules') / Path('slice-mesh.wasi.wasm')))

    pipeline_outputs: List[PipelineOutput] = [
        PipelineOutput(InterfaceTypes.Mesh),
    ]

    pipeline_inputs: List[PipelineInput] = [
        PipelineInput(InterfaceTypes.Mesh, input_mesh),
        PipelineInput(InterfaceTypes.JsonCompatible, planes),
    ]

    args: List[str] = ['--memory-io',]
    # Inputs
    args.append('0')
    args.append('1')
    # Outputs
    polylines_name = '0'
    args.append(polylines_name)

    # Options
    input_count = len(pipeline_inputs)

    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = outputs[0].data
    return result


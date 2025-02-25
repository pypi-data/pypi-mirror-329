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

async def slice_mesh_async(
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
    js_module = await js_package.js_module
    web_worker = js_resources.web_worker

    kwargs = {}

    outputs = await js_module.sliceMesh(to_js(input_mesh), to_js(planes), webWorker=web_worker, noCopy=True, **kwargs)

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

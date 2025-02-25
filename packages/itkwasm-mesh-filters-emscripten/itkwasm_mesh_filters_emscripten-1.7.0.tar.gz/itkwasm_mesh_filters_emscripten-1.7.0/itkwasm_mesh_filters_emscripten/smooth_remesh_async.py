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

async def smooth_remesh_async(
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
    js_module = await js_package.js_module
    web_worker = js_resources.web_worker

    kwargs = {}
    if number_points:
        kwargs["numberPoints"] = to_js(number_points)
    if triangle_shape_adaptation:
        kwargs["triangleShapeAdaptation"] = to_js(triangle_shape_adaptation)
    if triangle_size_adaptation:
        kwargs["triangleSizeAdaptation"] = to_js(triangle_size_adaptation)
    if normal_iterations:
        kwargs["normalIterations"] = to_js(normal_iterations)
    if lloyd_iterations:
        kwargs["lloydIterations"] = to_js(lloyd_iterations)
    if newton_iterations:
        kwargs["newtonIterations"] = to_js(newton_iterations)
    if newton_m:
        kwargs["newtonM"] = to_js(newton_m)
    if lfs_samples:
        kwargs["lfsSamples"] = to_js(lfs_samples)

    outputs = await js_module.smoothRemesh(to_js(input_mesh), webWorker=web_worker, noCopy=True, **kwargs)

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

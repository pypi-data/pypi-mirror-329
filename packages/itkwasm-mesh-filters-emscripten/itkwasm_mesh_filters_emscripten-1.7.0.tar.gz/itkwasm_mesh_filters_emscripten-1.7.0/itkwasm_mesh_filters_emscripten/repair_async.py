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

async def repair_async(
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
    js_module = await js_package.js_module
    web_worker = js_resources.web_worker

    kwargs = {}
    if merge_tolerance:
        kwargs["mergeTolerance"] = to_js(merge_tolerance)
    if minimum_component_area:
        kwargs["minimumComponentArea"] = to_js(minimum_component_area)
    if maximum_hole_area:
        kwargs["maximumHoleArea"] = to_js(maximum_hole_area)
    if maximum_hole_edges:
        kwargs["maximumHoleEdges"] = to_js(maximum_hole_edges)
    if maximum_degree3_distance:
        kwargs["maximumDegree3Distance"] = to_js(maximum_degree3_distance)
    if remove_intersecting_triangles:
        kwargs["removeIntersectingTriangles"] = to_js(remove_intersecting_triangles)

    outputs = await js_module.repair(to_js(input_mesh), webWorker=web_worker, noCopy=True, **kwargs)

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

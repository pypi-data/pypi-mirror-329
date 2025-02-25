# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
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
    func = environment_dispatch("itkwasm_mesh_filters", "repair")
    output = func(input_mesh, merge_tolerance=merge_tolerance, minimum_component_area=minimum_component_area, maximum_hole_area=maximum_hole_area, maximum_hole_edges=maximum_hole_edges, maximum_degree3_distance=maximum_degree3_distance, remove_intersecting_triangles=remove_intersecting_triangles)
    return output

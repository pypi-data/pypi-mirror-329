# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
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
    func = environment_dispatch("itkwasm_mesh_filters", "smooth_remesh")
    output = func(input_mesh, number_points=number_points, triangle_shape_adaptation=triangle_shape_adaptation, triangle_size_adaptation=triangle_size_adaptation, normal_iterations=normal_iterations, lloyd_iterations=lloyd_iterations, newton_iterations=newton_iterations, newton_m=newton_m, lfs_samples=lfs_samples)
    return output

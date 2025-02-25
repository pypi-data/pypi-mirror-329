# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    Mesh,
)

def keep_largest_component(
    input_mesh: Mesh,
) -> Mesh:
    """Keep only the largest component in the mesh.

    :param input_mesh: The input mesh.
    :type  input_mesh: Mesh

    :return: The output mesh with only the largest component.
    :rtype:  Mesh
    """
    func = environment_dispatch("itkwasm_mesh_filters", "keep_largest_component")
    output = func(input_mesh)
    return output

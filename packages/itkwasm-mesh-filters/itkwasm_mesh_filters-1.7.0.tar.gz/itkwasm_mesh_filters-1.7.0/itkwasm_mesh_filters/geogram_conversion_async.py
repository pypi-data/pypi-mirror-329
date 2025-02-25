# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
    Mesh,
)

async def geogram_conversion_async(
    input_mesh: Mesh,
) -> Mesh:
    """A test for reading and writing with geogram, itk::QuadEdgeMesh meshes

    :param input_mesh: The input mesh
    :type  input_mesh: Mesh

    :return: The output mesh
    :rtype:  Mesh
    """
    func = environment_dispatch("itkwasm_mesh_filters", "geogram_conversion_async")
    output = await func(input_mesh)
    return output

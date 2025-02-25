# Generated file. Do not edit.

import os
from typing import Dict, Tuple, Optional, List, Any

from itkwasm import (
    environment_dispatch,
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
    func = environment_dispatch("itkwasm_mesh_filters", "slice_mesh_async")
    output = await func(input_mesh, planes)
    return output

"""Conversions to and from Rhino.Geometry objects."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import RHINO

__all__ = []

if RHINO:
    from .compas_to_rhino import (  # noqa: E401
        box_to_rhino_box,
        frame_to_rhino_plane,
        line_to_rhino_line,
        matrix_to_rhino_transform,
        mesh_to_rhino_mesh,
        plane_to_rhino_plane,
        point_to_rhino_point,
        transformation_to_rhino_transform,
        vector_to_rhino_vector,
    )
    from .rhino_to_compas import (  # noqa: E401
        rhino_box_to_box,
        rhino_line_to_line,
        rhino_mesh_to_mesh,
        rhino_plane_to_frame,
        rhino_plane_to_plane,
        rhino_point_to_point,
        rhino_transform_to_matrix,
        rhino_transform_to_transformation,
        rhino_vector_to_vector,
    )

    __all__ += [
        "box_to_rhino_box",
        "frame_to_rhino_plane",
        "line_to_rhino_line",
        "matrix_to_rhino_transform",
        "mesh_to_rhino_mesh",
        "plane_to_rhino_plane",
        "point_to_rhino_point",
        "rhino_box_to_box",
        "rhino_line_to_line",
        "rhino_mesh_to_mesh",
        "rhino_mesh_to_mesh",
        "rhino_plane_to_frame",
        "rhino_plane_to_plane",
        "rhino_point_to_point",
        "rhino_transform_to_matrix",
        "rhino_transform_to_transformation",
        "rhino_vector_to_vector",
        "transformation_to_rhino_transform",
        "vector_to_rhino_vector",
    ]

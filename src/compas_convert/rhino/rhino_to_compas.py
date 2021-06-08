"""Conversions from Rhino.Geometry objects."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
from compas.datastructures import Mesh as cgMesh
from compas_rhino.geometry import RhinoMesh

from compas_convert import register_converter

try:
    from typing import List
except ImportError:
    pass


try:
    import Rhino.Geometry as rg
except ImportError:
    pass

RHINO_POINT_CLASSES = [
    rg.Point3d,
    rg.Point3f,
    rg.Point2d,
    rg.Point2f,
    rg.Point4d,
]

RHINO_VECTOR_CLASSES = [rg.Vector3d, rg.Vector3f, rg.Vector2d, rg.Vector2f]


@register_converter(
    RHINO_POINT_CLASSES + RHINO_VECTOR_CLASSES,
    cg.Point,
)
def rhino_point_to_point(pt):
    # type: (rg.Point3d) -> cg.Point
    """Convert :class:`Rhino.Geometry.Point3d` to :class:`compas.geometry.Point`."""
    return cg.Point(pt.X, pt.Y, z=getattr(pt, "Z", None))


@register_converter(
    RHINO_VECTOR_CLASSES + RHINO_POINT_CLASSES,
    cg.Vector,
)
def rhino_vector_to_vector(v):
    # type: (rg.Vector3d) -> cg.Vector
    """Convert :class:`Rhino.Geometry.Vector3d` to :class:`compas.geometry.Vector`."""
    return cg.Vector(v.X, v.Y, z=getattr(v, "Z", None))


# TODO: Handle rg.LineCurve and rg.PolyLine (if one segment)
@register_converter([rg.Line], cg.Line)
def rhino_line_to_line(line):
    # type: (rg.Line) -> cg.Line
    """Convert :class:`Rhino.Geometry.Line` to :class:`compas.geometry.Line`."""
    return cg.Line(rhino_point_to_point(line.From), rhino_point_to_point(line.To))


@register_converter([rg.Plane], cg.Plane)
def rhino_plane_to_plane(plane):
    # type: (rg.Plane) -> cg.Plane
    """Convert :class:`Rhino.Geometry.Plane` to :class:`compas.geometry.Plane`.

    Notes
    -----
    Unlike a :class:`Rhino.Geometry.Plane` the :class:`compas.geometry.Plane`
    does not store X-axis and Y-axis vectors. See
    :meth:`compas.geometry.Frame.from_plane` docstring.
    """
    return cg.Plane(
        rhino_point_to_point(plane.Origin), rhino_vector_to_vector(plane.Normal)
    )


@register_converter([rg.Plane], cg.Frame)
def rhino_plane_to_frame(plane):  # type: (rg.Plane) -> cg.Frame
    """Convert :class:`Rhino.Geometry.Plane` to :class:`compas.geometry.Frame`."""
    pt = rhino_point_to_point(plane.Origin)
    xaxis = rhino_vector_to_vector(plane.XAxis)
    yaxis = rhino_vector_to_vector(plane.YAxis)
    return cg.Frame(pt, xaxis, yaxis)


@register_converter([rg.Transform], list())
def rhino_transform_to_matrix(rgT):
    # type: (rg.Transform) -> List[List[float]]
    """Convert :class:`Rhino.Geometry.Transform` to transformation matrix."""
    return [[rgT.Item[i, j] for j in range(4)] for i in range(4)]  # type: ignore


@register_converter([rg.Transform], cg.Transformation)
def rhino_transform_to_transformation(rgT):
    # type: (rg.Transform) -> cg.Transformation
    M = rhino_transform_to_matrix(rgT)
    return cg.Transformation.from_matrix(M)


@register_converter([rg.Mesh], cgMesh)
def rhino_mesh_to_mesh(mesh, cls=None):  # type: (rg.Mesh, cgMesh) -> cgMesh
    """Convert :class:`Rhino.Geometry.Mesh` to :class:`compas.datastructures.Mesh`."""
    return RhinoMesh.from_geometry(mesh).to_compas(cls=cls)


@register_converter([rg.Box], cg.Box)
def rhino_box_to_box(box):  # type: (rg.Box) -> cg.Box
    """Convert a :class:`Rhino.Geometry.Box` to a :class:`compas.geometry.Box`."""
    diagonal_rhino_pts = [box.PointAt(0, 0, 0), box.PointAt(1, 1, 1)]

    diagonal_compas_pts = [rhino_point_to_point(p) for p in diagonal_rhino_pts]
    return cg.Box.from_diagonal(diagonal_compas_pts)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry as cg
from compas.datastructures import Mesh as cgMesh
from compas_ghpython.utilities import draw_mesh

from compas_convert import register_converter

try:
    import Rhino.Geometry as rg  # type: ignore
except ImportError:
    compas.raise_if_ironpython()

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence


@register_converter([cg.Point, cg.Vector], rg.Point3d)
def point_to_rhino_point(pt):  # type: (compas.geometry.Point) -> rg.Point3d
    """Convert :class:`compas.geometry.Point` to :class:`Rhino.Geometry.Point3d`."""
    return rg.Point3d(*pt.data)


@register_converter([cg.Vector, cg.Point], rg.Vector3d)
def vector_to_rhino_vector(
    v,
):  # type: (compas.geometry.Vector) -> rg.Vector3d
    """Convert :class:`compas.geometry.Vector` to :class:`Rhino.Geometry.Vector3d`."""
    return rg.Vector3d(*v.data)


@register_converter([cg.Line], rg.Line)
def line_to_rhino_line(line):  # type: (compas.geometry.Line) -> rg.Line
    """Convert :class:`compas.geometry.Line` to :class:`Rhino.Geometry.Line`."""
    return rg.Line(point_to_rhino_point(line.start), point_to_rhino_point(line.end))


@register_converter([cg.Plane, cg.Frame], rg.Plane)
def plane_to_rhino_plane(
    plane,
):  # type: (cg.Plane) -> rg.Plane
    """Convert :class:`compas.geometry.Plane` to :class:`Rhino.Geometry.Plane`."""
    return rg.Plane(
        point_to_rhino_point(plane.point), vector_to_rhino_vector(plane.normal)
    )


@register_converter([cg.Frame], rg.Plane)
def frame_to_rhino_plane(
    frame,
):  # type: (cg.Frame) -> rg.Plane
    """Convert :class:`compas.geometry.Frame` to :class:`Rhino.Geometry.Plane`."""
    o = point_to_rhino_point(frame.point)
    x = vector_to_rhino_vector(frame.xaxis)
    y = vector_to_rhino_vector(frame.yaxis)
    return rg.Plane(o, x, y)


@register_converter([cg.Box], rg.Box)
def box_to_rhino_box(box):  # type: (cg.Box) -> rg.Box
    """Convert :class:`compas.geometry.Box` to a :class:`Rhino.Geometry.Box`."""
    plane = frame_to_rhino_plane(box.frame)

    sizes = (box.xsize, box.ysize, box.zsize)
    intervals = [rg.Interval(-size / 2, size / 2) for size in sizes]

    return rg.Box(plane, *intervals)


@register_converter([list], rg.Transform)
def matrix_to_rhino_transform(M):  # type: (Sequence[Sequence[float]]) -> rg.Transform
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix."""
    rgM = rg.Transform()
    for i, row in enumerate(M):
        for j, val in enumerate(row):
            rgM[i, j] = val  # type: ignore
    return rgM


@register_converter([cg.Transformation], rg.Transform)
def transformation_to_rhino_transform(
    xform,
):  # type: (cg.TransformatioN) -> rg.Transform
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix."""
    return matrix_to_rhino_transform(xform.matrix)


@register_converter([cgMesh], rg.Mesh)
def mesh_to_rhino_mesh(mesh):
    """Convert :class:`compas.datastructures.Mesh` to :class:`Rhino.Geometry.Mesh`."""
    return draw_mesh(*mesh.to_vertices_and_faces())

"""Most of these are in compas >=0.15 but compas_fab is not there yet."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
from compas_ghpython.artists import MeshArtist

try:
    import Rhino  # type: ignore
    import Rhino.Geometry as rg  # type: ignore
except ImportError:
    compas.raise_if_ironpython()


def point_to_rhino_point(pt):  # type: (compas.geometry.Point) -> Rhino.Geometry.Point3d
    """Convert :class:`compas.geometry.Point` to :class:`Rhino.Geometry.Point3d`.

    Parameters
    ----------
    pt : :class:`compas.geometry.Point`
        Point object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Point3d`
        Resulting Point3d object.
    """
    return rg.Point3d(*pt.data)


def vector_to_rhino_vector(
    v,
):  # type: (compas.geometry.Vector) -> Rhino.Geometry.Vector3d
    """Convert :class:`compas.geometry.Vector` to :class:`Rhino.Geometry.Vector3d`.

    Parameters
    ----------
    v : :class:`compas.geometry.Vector`
        Vector object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Vector3d`
        Resulting Vector3d object.
    """
    return rg.Vector3d(*v.data)


def line_to_rhino_line(line):  # type: (compas.geometry.Line) -> Rhino.Geometry.Line
    """Convert :class:`compas.geometry.Line` to :class:`Rhino.Geometry.Line`.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        Point object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Line`
        Resulting Line object.
    """
    return rg.Line(point_to_rhino_point(line.start), point_to_rhino_point(line.end))


def plane_to_rhino_plane(
    cgplane,
):  # type: (compas.geometry.Plane) -> Rhino.Geometry.Plane
    """Convert :class:`compas.geometry.Plane` to :class:`Rhino.Geometry.Plane`.

    Parameters
    ----------
    cgplane : :class:`compas.geometry.Plane`
        Plane to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
        Resulting plane.
    """
    return rg.Plane(
        point_to_rhino_point(cgplane.point), vector_to_rhino_vector(cgplane.normal)
    )


def frame_to_rhino_plane(
    frame,
):  # type: (compas.geometry.Frame) -> Rhino.Geometry.Plane
    """Convert :class:`compas.geometry.Frame` to :class:`Rhino.Geometry.Plane`.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        Frame to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
        Resulting plane.
    """
    o = point_to_rhino_point(frame.point)
    x = vector_to_rhino_vector(frame.xaxis)
    y = vector_to_rhino_vector(frame.yaxis)
    return rg.Plane(o, x, y)


def matrix_to_rhino_transform(M):
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix.

    Parameters
    ----------
    M : :class:`list` of :class:`list` of :class:`float`
        Transformation matrix.

    Returns
    -------
    :class:`Rhino.Geometry.Transform`
    """
    rgM = rg.Transform()
    for i, row in enumerate(M):
        for j, val in enumerate(row):
            rgM[i, j] = val
    return rgM


def mesh_to_rhino_mesh(mesh):
    """Convert :class:`compas.datastructures.Mesh` to :class:`Rhino.Geometry.Mesh`."""
    artist = MeshArtist(mesh)

    return artist.draw_mesh()

"""Conversions from Rhino.Geometry objects."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry as cg
from compas_rhino.geometry import RhinoMesh

try:
    import Rhino  # type: ignore
except ImportError:
    compas.raise_if_ironpython()


def rhino_point_to_point(pt):
    # type: (Rhino.Geometry.Point3d) -> compas.geometry.Point
    """Convert :class:`Rhino.Geometry.Point3d` to :class:`compas.geometry.Point`.

    Parameters
    ----------
    pt : :class:`Rhino.Geometry.Point3d`
        Plane object to convert
    Returns
    -------
    :class:`compas.geometry.Point`
        Resulting point object
    """
    return cg.Point(pt.X, pt.Y, pt.Z)


def rhino_vector_to_vector(v):
    # type: (Rhino.Geometry.Vector3d) -> compas.geometry.Vector
    """Convert :class:`Rhino.Geometry.Vector3d` to :class:`compas.geometry.Vector`.

    Parameters
    ----------
    v : :class:`Rhino.Geometry.Vector3d`
        Vector object to convert
    Returns
    -------
    :class:`compas.geometry.Vector`
        Resulting vector object
    """
    return cg.Vector(v.X, v.Y, v.Z)


def rhino_line_to_line(line):
    # type: (Rhino.Geometry.Line) -> compas.geometry.Line
    """Convert :class:`Rhino.Geometry.Line` to :class:`compas.geometry.Line`.

    Parameters
    ----------
    line : :class:`Rhino.Geometry.Line`
        Line object to convert
    Returns
    -------
    :class:`compas.geometry.Line`
        Resulting line object
    """
    return cg.Line(rhino_point_to_point(line.From), rhino_point_to_point(line.To))


def rhino_plane_to_plane(plane):
    # type: (Rhino.Geometry.Plane) -> compas.geometry.Plane
    """Convert :class:`Rhino.Geometry.Plane` to :class:`compas.geometry.Plane`.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`
        Plane object to convert
    Returns
    -------
    :class:`compas.geometry.Plane`
        Resulting plane object
    Notes
    -----
    Unlike a :class:`Rhino.Geometry.Plane` the :class:`compas.geometry.Plane`
    does not store X-axis and Y-axis vectors. See
    :meth:`compas.geometry.Frame.from_plane` docstring.
    """
    return cg.Plane(
        rhino_point_to_point(plane.Origin), rhino_vector_to_vector(plane.Normal)
    )


def rhino_plane_to_frame(plane):
    # type: (Rhino.Geometry.Plane) -> compas.geometry.Frame
    """Convert :class:`Rhino.Geometry.Plane` to :class:`compas.geometry.Frame`.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`
        Plane object to convert
    Returns
    -------
    :class:`compas.geometry.Frame`
        Resulting frame object
    """
    pt = rhino_point_to_point(plane.Origin)
    xaxis = rhino_vector_to_vector(plane.XAxis)
    yaxis = rhino_vector_to_vector(plane.YAxis)
    return cg.Frame(pt, xaxis, yaxis)


def rhino_transform_to_matrix(rgM):
    # type: (Rhino.Geometry.Transform) -> list
    """Convert :class:`Rhino.Geometry.Transform` to transformation matrix.

    Parameters
    ----------
    rgM : :class:`Rhino.Geometry.Transform`
    Returns
    -------
    :class:`list` of :class:`list` of :class:`float`.
    """
    M = [[rgM.Item[i, j] for j in range(4)] for i in range(4)]
    return M


def rhino_mesh_to_mesh(mesh, cls=None):
    return RhinoMesh.from_geometry(mesh).to_compas(cls=cls)

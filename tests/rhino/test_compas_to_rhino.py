from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
from compas import RHINO

from compas_convert.rhino import frame_to_rhino_plane
from compas_convert.rhino import line_to_rhino_line
from compas_convert.rhino import matrix_to_rhino_transform
from compas_convert.rhino import point_to_rhino_point
from compas_convert.rhino import vector_to_rhino_vector

if RHINO:
    import Rhino.Geometry as rg  # type: ignore


def test_point_to_rhino_point():
    point = point_to_rhino_point(cg.Point(1, 2, 3))
    if point.Z != 3.0:
        raise Exception()


def test_vector_to_rhino_vector():
    vector = vector_to_rhino_vector(cg.Vector(5, 1, 9))
    if not vector.Unitize():
        raise Exception()


def test_line_to_rhino_line():
    line = line_to_rhino_line(cg.Line([1, 2, 3], [3, 2, 1]))
    if line.Direction != rg.Vector3d(2, 0, -2):
        raise Exception()


def test_frame_to_rhino_plane():
    plane = frame_to_rhino_plane(cg.Frame([1, 3, -1], [1, 1, 2], [0, 1, 1]))
    if not isinstance(plane.Normal, rg.Vector3d):
        raise Exception()

    # matrix_to_rgtransform
    R = cg.Rotation.from_basis_vectors([1, 2, 0], [2, 1, 3])
    if not isinstance(matrix_to_rhino_transform(R), rg.Transform):
        raise Exception()


if __name__ == "__main__":
    test_point_to_rhino_point()
    test_vector_to_rhino_vector()

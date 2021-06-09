from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import RHINO

from compas_convert.rhino import rhino_line_to_line
from compas_convert.rhino import rhino_plane_to_frame
from compas_convert.rhino import rhino_point_to_point
from compas_convert.rhino import rhino_transform_to_matrix
from compas_convert.rhino import rhino_vector_to_vector

if RHINO:
    import Rhino.Geometry as rg  # type: ignore


def test_rhino_point_to_point():
    pt = rhino_point_to_point(rg.Point3d(3, 2, 1))
    if pt.data != [3.0, 2.0, 1.0]:
        raise Exception("rgpoint_to_cgpoint failed")


def test_rhino_vector_to_vector():
    v = rhino_vector_to_vector(rg.Vector3d(3, 2, 1))
    if not v.length > 3.7 and not v.length < 3.8:
        raise Exception("rgvector_to_cgvector failed")


def test_rhino_line_to_line():
    line = rhino_line_to_line(rg.Line(rg.Point3d(3, 2, 1), rg.Vector3d(1, 1, 0), 5.0))
    if not isinstance(line.midpoint.z, float):
        raise Exception("rgline_to_cgline failed")


def test_rhino_plane_to_frame():
    frame = rhino_plane_to_frame(rg.Plane(rg.Point3d(1, 3, 2), rg.Vector3d(2, -1, 1)))
    if (
        frame.quaternion.__repr__
        != "Quaternion(0.713799, 0.462707, 0.285969, 0.441152)"
    ):
        raise Exception("rgplane_to_cgframe failed")


def test_rhino_transform_to_matrix():
    matrix = rg.Transform.ZeroTransformation

    zero_matrix = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    if rhino_transform_to_matrix(matrix) != zero_matrix:
        raise Exception("rgtransform_to_matrix failed.")


if __name__ == "__main__":
    test_rhino_point_to_point()
    test_rhino_vector_to_vector()

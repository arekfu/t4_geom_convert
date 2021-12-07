# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :
'''Tests for the :mod:`~.VectUtils` module.'''
# pylint: disable=no-value-for-parameter

from math import isclose, fabs

from hypothesis import given, assume, note
from hypothesis.strategies import floats, tuples, composite

import numpy as np

from t4_geom_convert.Kernel.VectUtils import (scal, rescale, vdiff, renorm,
                                              mag, mag2,
                                              pointInPlaneIntersection,
                                              rotation_from_vectors)


def is_in_plane(point, plane):
    '''Returns `True` if the point lies in the given plane.'''
    pl_pt, norm = plane
    dist = scal(vdiff(point, pl_pt), norm)
    note('dist: {}'.format(dist))
    return isclose(dist, 0., abs_tol=1e-8)


def is_parallel(vector1, vector2):
    '''Returns `True` if the vectors are parallel'''
    scal_prod = scal(vector1, vector2)
    mag_prod = mag(vector1)*mag(vector2)
    note('scal_prod: {}'.format(scal_prod))
    note('mag_prod: {}'.format(mag_prod))
    return isclose(scal_prod, mag_prod)


@composite
def vectors(draw, *, norm=None):
    '''Generate random vectors, possibly with a given norm.'''
    a_vec = draw(tuples(floats(min_value=-1e3, max_value=1e3),
                        floats(min_value=-1e3, max_value=1e3),
                        floats(min_value=-1e3, max_value=1e3)))
    if norm is None:
        return a_vec
    assume(mag2(a_vec) > 0.)
    return renorm(a_vec, norm)


@given(point1=vectors(), point2=vectors(),
       normal1=vectors(norm=1.), normal2=vectors(norm=1.))
def test_intersection(point1, point2, normal1, normal2):
    '''Test that the point generated by :func:`~.pointInPlaneIntersection`
    always lies in both planes.'''
    assume(not isclose(fabs(scal(normal1, normal2)), 1.))
    plane1 = (point1, normal1)
    plane2 = (point2, normal2)
    int_p, line_vec = pointInPlaneIntersection(plane1, plane2)
    assert is_in_plane(int_p, plane1)
    assert is_in_plane(int_p, plane2)
    assert isclose(scal(line_vec, normal1), 0., abs_tol=1e-10)
    assert isclose(scal(line_vec, normal2), 0., abs_tol=1e-10)


@given(vector1=vectors(), vector2=vectors())
def test_rotation_from_vectors(vector1, vector2):
    '''Test that :func:`~.rotation_from_vectors` actually rotates `vector1` on
    top of `vector2`.
    '''
    assume(mag2(vector1) > 1e-5)
    assume(mag2(vector2) > 1e-5)
    assume(not is_parallel(rescale(-1.0, vector1), vector2))
    mat = rotation_from_vectors(vector1, vector2)
    new_vector2 = np.dot(mat, np.array(vector1))
    assert is_parallel(vector2, new_vector2)


@given(vector1=vectors(), vector2=vectors())
def test_rotation_unitary(vector1, vector2):
    '''Test that the matrix given by :func:`~.rotation_from_vectors` is
    unitary.
    '''
    assume(mag2(vector1) > 1e-5)
    assume(mag2(vector2) > 1e-5)
    assume(not is_parallel(rescale(-1.0, vector1), vector2))
    mat = rotation_from_vectors(vector1, vector2)
    assert np.allclose(mat.dot(mat.T), np.identity(3))
    assert np.allclose(mat.T.dot(mat), np.identity(3))

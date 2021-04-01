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
'''Unit tests for the :mod:`~.Lattice` module.'''
# pylint: disable=no-value-for-parameter

from math import isclose, fabs, sqrt
from hypothesis import given, assume, note, settings, event
from hypothesis.strategies import floats, composite, lists

from t4_geom_convert.Kernel.Volume.Lattice import latticeReciprocal
from t4_geom_convert.Kernel.VectUtils import scal, vect


@composite
def vectors(draw):
    '''Generate a random three-dimensional vector.'''
    component = floats(-1e5, 1e5, allow_nan=False, allow_infinity=False)
    vec = draw(component), draw(component), draw(component)
    assume(scal(vec, vec) > 1e-5)
    return vec


@composite
def lattices(draw):
    '''Generate base vectors for a 1D, 2D or 3D square lattice. Make sure that
    they are not collinear.'''
    vecs = draw(lists(vectors(), min_size=1, max_size=3))
    for i, vec in enumerate(vecs):
        for j, other in enumerate(vecs[i + 1:]):
            cosangle = fabs(scal(vec, other)) / sqrt(scal(vec, vec)
                                                     * scal(other, other))
            note('cos(angle {}^{}) = {}'.format(i, j + i + 1, cosangle))
            assume(cosangle < 1 - 1e-5)
    if len(vecs) == 3:
        # check that the vectors are not coplanar
        rel_volume = fabs(scal(vecs[0], vect(vecs[1], vecs[2]))
                          / sqrt(scal(vecs[0], vecs[0])
                                 * scal(vecs[1], vecs[1])
                                 * scal(vecs[2], vecs[2])))
        assume(rel_volume > 1e-5)
        note('volume of the parallelepiped / cube = {}'.format(rel_volume))
    return vecs


def latticeReciprocalTest(vecs):
    '''Call :func:`~.latticeReciprocal`, and additionally test that the list of
    vectors it returns has the same length as the argument.'''
    recs = latticeReciprocal(vecs)
    assert len(recs) == len(vecs)
    note('reciprocal lattice: {}'.format(recs))
    return recs


@settings(max_examples=2000)
@given(lattice=lattices())
def test_bravais_property(lattice):
    r'''Test that the reciprocal vectors of a 1D, 2D or 3D lattice satisfy the
    Bravais property:

    .. math::

        v_i \cdot r_j = delta_{ij}, i,j=1,2,3
    '''
    event('lattice dimension = {}'.format(len(lattice)))
    rec_lattice = latticeReciprocalTest(lattice)
    for i, lhs in enumerate(lattice):
        for j, rhs in enumerate(rec_lattice):
            scalar = scal(lhs, rhs)
            expected = 1.0 if i == j else 0.0
            msg = ('Bravais property failed for vecs {} vs. {}: scalar = {}'
                   .format(i, j, scalar))
            assert isclose(expected, scalar, abs_tol=1e-5), msg

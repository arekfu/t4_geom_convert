# -*- coding: utf-8 -*-
'''
:author: Davide Mancusi
:date: 2019-09-19
'''

from math import sqrt

def scal(v1, v2):
    '''Yields the scalar product of `v1` and `v2`.'''
    a1, b1, c1 = v1
    a2, b2, c2 = v2
    result = a1*a2 + b1*b2 + c1*c2
    return float(result)

def vect(v1, v2):
    '''Yields the vector product of `v1` and `v2`.'''
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    result = (y1*z2-z1*y2,x2*z1-x1*z2,x1*y2-y1*x2)
    return result

def mixed(v1, v2, v3):
    '''Yields the mixed product of `v1`, `v2` and `v3`.

    The mixed product is defined as `v1 · (v2 × v3)` and is equal to the
    determinant of the matrix having the components of `v1`, `v2` and `v3` as
    rows.
    '''
    return scal(v1, vect(v2, v3))

def rescale(a, v1):
    '''Return `v1` multiplied by a scalar `a`, as a new vector.'''
    x1, y1, z1 = v1
    return (a*x1, a*y1, a*z1)

def vsum(*args):
    '''Return the vector sum of its arguments.'''
    xsum = 0.
    ysum = 0.
    zsum = 0.
    for vec in args:
        xsum += vec[0]
        ysum += vec[1]
        zsum += vec[2]
    return xsum, ysum, zsum

def vdiff(v1, v2):
    '''Return the vector difference of `v1` and `v2` (`v1-v2`).'''
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return (x1-x2, y1-y2, z1-z2)

def planeParamsFromPoints(pt1, pt2, pt3):
    '''Compute the parameters `(a ,b, c, d)` of the plane passing through the
    three given points `pt1`, `pt2`, `pt3`.

    The equation of the plane is written in the MCNP form as

    .. math::

        a x + b y + c z - d = 0
    '''
    d12 = vdiff(pt1, pt2)
    d13 = vdiff(pt1, pt3)
    normal = vect(d12, d13)
    normal_len2 = scal(normal, normal)
    if normal_len2 <= 1e-10:
        raise ValueError('Cannot convert plane from three points because the '
                         'points are collinear or almost so: {}, {}, {}'
                         .format(pt1, pt2, pt3))
    unit_normal = rescale(1./sqrt(normal_len2), normal)
    pos = scal(unit_normal, pt1)
    return [unit_normal[0], unit_normal[1], unit_normal[2], pos]

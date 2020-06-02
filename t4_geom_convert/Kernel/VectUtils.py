# -*- coding: utf-8 -*-
'''
:author: Davide Mancusi
:date: 2019-09-19
'''

from math import sqrt, cos, sin, isclose


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
    result = (y1*z2-z1*y2, x2*z1-x1*z2, x1*y2-y1*x2)
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


def renorm(vec, norm=1.):
    '''Return a new vector parallel to `vec` whose norm is equal to `norm`.'''
    return rescale(norm/mag(vec), vec)


def mag2(vec):
    '''Return the square of the magnitude of `vec`.'''
    return scal(vec, vec)


def mag(vec):
    '''Return the magnitude of `vec`.'''
    return sqrt(mag2(vec))


def rotate(vec, axis, angle):
    r'''Rotate vector `vec` around the axis `axis` by angle `angle`, according
    to the right-hand rule.

    This function uses Rodrigues' rotation formula. If we denote `vec` as `v`,
    the angle as `θ` and the axis as `k`, the formula reads:

    .. math::

        v' = v \cos(\theta) + (k ^ v) \sin(\theta)
             + k (k\cdot v) (1 - \cos(\theta))

    Examples:

        >>> from math import pi
        >>> vec = (1, 1, 0)
        >>> axis = (0, 0, 1)
        >>> rot_vec = rotate(vec, axis, 0.5*pi)
        >>> print('({:.5f}, {:.5f}, {:.5f})'.format(*rot_vec))
        (-1.00000, 1.00000, 0.00000)
        >>> rot_vec = rotate(vec, axis, 0.25*pi)
        >>> print('({:.5f}, {:.5f}, {:.5f})'.format(*rot_vec))
        (0.00000, 1.41421, 0.00000)

    :param vec: the vector to rotate
    :param axis: the rotation axis (must be a unit vector)
    :param angle: the rotation angle, in radians
    '''
    cangle = cos(angle)
    sangle = sin(angle)
    term1 = rescale(cangle, vec)
    term2 = rescale(sangle, vect(axis, vec))
    term3 = rescale((1 - cangle)*scal(axis, vec), axis)
    return vsum(term1, term2, term3)


def planeParamsFromPoints(pt1, pt2, pt3):
    '''Compute the parameters `(a ,b, c, d)` of the plane passing through the
    three given points `pt1`, `pt2`, `pt3`.

    The equation of the plane is written in the MCNP form as

    .. math::

        a x + b y + c z - d = 0

    Furthermore, the normal to the plane is oriented in such as way that the
    origin has negative sense (this is the MCNP convention).
    '''
    d12 = vdiff(pt1, pt2)
    d13 = vdiff(pt1, pt3)
    normal = vect(d12, d13)
    normal_len2 = mag2(normal)
    if normal_len2 <= 1e-10:
        raise ValueError('Cannot convert plane from three points because the '
                         'points are collinear or almost so: {}, {}, {}'
                         .format(pt1, pt2, pt3))
    unit_normal = renorm(normal)
    pos = scal(unit_normal, pt1)

    epsilon = 1e-14
    params = [unit_normal[0], unit_normal[1], unit_normal[2], pos]
    flipped_params = [-unit_normal[0], -unit_normal[1], -unit_normal[2], -pos]

    if pos < -epsilon:
        # make sure the origin lies on the negative side of the plane
        return flipped_params
    if pos > epsilon:
        return params

    # Here we are in the D=0 case. The origin lies in the plane; ensure that
    # (0, 0, ∞) lies on the positive side of the plane
    if unit_normal[2] < -epsilon:
        return flipped_params
    if unit_normal[2] > epsilon:
        return params

    # Here we are in the D=C=0 case. Ensure that (0, ∞, 0) lies on the positive
    # side of the plane
    if unit_normal[1] < -epsilon:
        return flipped_params
    if unit_normal[1] > epsilon:
        return params

    # Here we are in the D=C=B=0 case. Ensure that (∞, 0, 0) lies on the
    # positive side of the plane
    if unit_normal[0] < -epsilon:
        return flipped_params
    if unit_normal[0] > epsilon:
        return params

    # What are we even doing here?
    raise ValueError('Cannot convert plane from three points because the '
                     'points are collinear or almost so: {}, {}, {}'
                     .format(pt1, pt2, pt3))

def planeParamsFromNormalAndPoint(normal, point):
    '''Return the MCNP-style parameters of the plane having the given normal
    and passing through the given points.'''
    intercept = scal(normal, point)
    return [normal[0], normal[1], normal[2], intercept]


def pointInPlaneIntersection(plane1, plane2):
    '''Construct a point in the intersection of two planes. The planes must be
    given as a `(point, normal)` pair.

    >>> from math import isclose
    >>> def is_in_plane(point, plane):
    ...     pt, norm = plane
    ...     return isclose(scal(vdiff(point, pt), norm), 0., abs_tol=1e-10)

    >>> plane1 = ((0, 0, 0), (1, 0, 0))
    >>> plane2 = ((0, 0, 0), (0, 1, 0))
    >>> pointInPlaneIntersection(plane1, plane2)
    ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0))

    >>> plane1 = ((0, 0, 0), (1, 0, 0))
    >>> plane2 = ((0, 5, 0), (0, 1, 0))
    >>> int_p, line_vec = pointInPlaneIntersection(plane1, plane2)
    >>> is_in_plane(int_p, plane1) and is_in_plane(int_p, plane2)
    True
    >>> isclose(scal(line_vec, (1, 0, 0)), 0., abs_tol=1e-10)
    True
    >>> isclose(scal(line_vec, (0, 1, 0)), 0., abs_tol=1e-10)
    True
    '''
    point1, normal1 = plane1
    point2, normal2 = plane2
    # line_vec is the vector of the line where the two planes intersect
    line_vec = vect(normal1, normal2)
    vec1 = vect(normal1, line_vec)
    vec2 = vect(normal2, line_vec)
    dist = vdiff(point1, point2)
    a = - mixed(dist, vec2, line_vec) / mixed(vec1, vec2, line_vec)
    int_point = vsum(point1, rescale(a, vec1))
    return int_point, renorm(line_vec)


def planeSide(point, plane):
    '''Returns 1 if point lies on the positive side of the plane, -1 if it lies
    on the negative side and 0 if it lies on the plane (no numerical
    tolerance).'''
    point_pl, normal = plane
    dist = scal(vdiff(point, point_pl), normal)
    if dist > 0:
        return 1
    if dist < 0:
        return -1
    return 0


def projectPointOnPlane(point, plane, direction):
    '''Project a point on a plane along the given direction.

    >>> from math import isclose, sqrt
    >>> point = (0, 0, 3)
    >>> plane = ((0, 0, 0), (0, 0, 1))
    >>> direction = (1, 0, 1)
    >>> proj = projectPointOnPlane(point, plane, direction)
    >>> expected = (-3, 0, 0)
    >>> all(isclose(p, e, abs_tol=1e-10) for p, e in zip(proj, expected))
    True

    >>> point = (0, 0, 3)
    >>> plane = ((0, 0, 1), (0, 0, 1))
    >>> direction = (2, 0, 1)
    >>> proj = projectPointOnPlane(point, plane, direction)
    >>> expected = (-4, 0, 1)
    >>> all(isclose(p, e, abs_tol=1e-10) for p, e in zip(proj, expected))
    True
    '''
    pl_pt, normal = plane
    dist = scal(vdiff(pl_pt, point), normal)/scal(direction, normal)
    return vsum(point, rescale(dist, direction))


def isPointOnPlane(point, plane, *, tol=1e-10):
    '''Returns `True` if the point lies on the plane within the specified
    tolerance.

    >>> point = (1.0, 1.0, 1.0)
    >>> plane = ((3.0, 0.0, 0.0), (1.0, 1.0, 1.0))
    >>> isPointOnPlane(point, plane)
    True
    '''
    return isVectorParallelToPlane(vdiff(point, plane[0]), plane, tol=tol)


def isVectorParallelToPlane(vector, plane, *, tol=1e-10):
    '''Returns `True` if the vector is parallel to the plane within the
    specified tolerance.

    >>> vector = (1.0, 1.0, -2.0)
    >>> plane = ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0))
    >>> isVectorParallelToPlane(vector, plane)
    True
    >>> isVectorParallelToPlane(rescale(2.0, vector), plane)
    True
    >>> isVectorParallelToPlane(plane[1], plane)
    False
    '''
    return isclose(scal(plane[1], vector), 0.0, abs_tol=tol)


def transpose(matrix):
    '''Transpose a 3x3 matrix.

    >>> mat = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> transpose(mat)
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    '''
    assert len(matrix) == 9
    return [elem for i in range(3) for elem in matrix[i::3]]


def matrix_rows(matrix):
    '''Transform a 3x3 matrix into the list of its rows.

    >>> mat = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> matrix_rows(mat)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    '''
    assert len(matrix) == 9
    return [matrix[3*i:3*i+3] for i in range(3)]

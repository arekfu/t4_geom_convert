# -*- coding: utf-8 -*-
'''
:author: Davide Mancusi
:date: 2019-09-19
'''

import math

from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS
from ..Transformation.TransformationQuad import transformation_quad
from ..VectUtils import (vect, vsum, vdiff, scal, rescale, renorm, mag, mag2,
                         mixed, rotate, planeParamsFromPoints,
                         planeParamsFromNormalAndPoint)


class MacroBodyError(Exception):
    '''Error that is raised if the number of macrobody parameters differs from
    the expected number.'''
    def __init__(self, type_, expected, params):
        super().__init__('Wrong number of parameters for {} (expected {}): '
                         '{}'.format(type_, expected, params))


def check_params_length(type_, expected, params):
    '''Throw a :class:`MacroBodyError` if the number of parameters present does
    not match the expected number.'''
    if isinstance(expected, int):
        expected = (expected,)
    if len(params) not in expected:
        raise MacroBodyError(type_, expected, params)


def box(params):
    '''Transform the parameters of a BOX macrobody.

    This function is actually capable of handling generic parallelepipeds (MCNP
    mandates that the parallelepiped must be right).

    :param list params: the twelve MCNP parameters for ``BOX``
    :returns: a list of triples representing the surfaces that collectively
        describe the macrobody. The first element of each triple is the type of
        the surface; the second element is a list of coefficients; the third
        element is an integer (=±1) indicating on which side of the plane the
        macrobody lies; if the integer is +1, the **outside** of the macrobody
        lies in the "positive" direction for the surface.
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('BOX', 12, params)

    base = params[0:3]
    vec_a = params[3:6]
    vec_b = params[6:9]
    vec_c = params[9:]
    pt_a = vsum(base, vec_a)
    pt_b = vsum(base, vec_b)
    pt_c = vsum(base, vec_c)
    normal_ab = vect(vec_a, vec_b)
    normal_bc = vect(vec_b, vec_c)
    normal_ca = vect(vec_c, vec_a)
    # the side_* variables indicate which side of the plane points outside the
    # box
    side_ab = 1 if scal(normal_ab, vec_c) < 0. else -1
    side_bc = 1 if scal(normal_bc, vec_a) < 0. else -1
    side_ca = 1 if scal(normal_ca, vec_b) < 0. else -1

    return [
        (MS.P, planeParamsFromNormalAndPoint(normal_bc, pt_a), -side_bc),
        (MS.P, planeParamsFromNormalAndPoint(normal_bc, base), side_bc),
        (MS.P, planeParamsFromNormalAndPoint(normal_ca, pt_b), -side_ca),
        (MS.P, planeParamsFromNormalAndPoint(normal_ca, base), side_ca),
        (MS.P, planeParamsFromNormalAndPoint(normal_ab, pt_c), -side_ab),
        (MS.P, planeParamsFromNormalAndPoint(normal_ab, base), side_ab),
    ]


def rpp(params):
    '''Transform the parameters of an RPP macrobody.

    :param list params: the six MCNP parameters for ``RPP``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('RPP', 6, params)
    xmin, xmax, ymin, ymax, zmin, zmax = params
    return [
        (MS.P, [1, 0, 0, xmax], 1),
        (MS.P, [1, 0, 0, xmin], -1),
        (MS.P, [0, 1, 0, ymax], 1),
        (MS.P, [0, 1, 0, ymin], -1),
        (MS.P, [0, 0, 1, zmax], 1),
        (MS.P, [0, 0, 1, zmin], -1),
    ]


def sph(params):
    '''Transform the parameters of an SPH macrobody.

    :param list params: the four MCNP parameters for ``SPH``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('SPH', 4, params)
    return [(MS.S, params.copy(), 1)]


def rcc(params):
    '''Transform the parameters of an RCC macrobody.

    :param list params: the seven MCNP parameters for ``RCC``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('RCC', 7, params)
    base_bottom = params[0:3]
    height = params[3:6]
    radius = params[6]
    base_top = vsum(base_bottom, height)
    return [
        (MS.C, base_bottom + [radius] + height, 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_top), 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_bottom), -1),
    ]


def rhp(params):
    '''Transform the parameters of an RHP/HEX macrobody.

    :param list params: the fifteen MCNP parameters for ``RHP``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('RHP', (9, 15), params)
    base_bottom = params[0:3]
    height = params[3:6]
    vec_a = params[6:9]
    if len(params) == 15:
        vec_b = params[9:12]
        vec_c = params[12:]
    else:
        vec_b = rotate(vec_a, renorm(height), math.pi/3.)
        vec_c = rotate(vec_a, renorm(height), 2.*math.pi/3.)
    base_top = vsum(base_bottom, height)
    pt_a = vsum(base_bottom, vec_a)
    pt_b = vsum(base_bottom, vec_b)
    pt_c = vsum(base_bottom, vec_c)
    pt_a_op = vdiff(base_bottom, vec_a)
    pt_b_op = vdiff(base_bottom, vec_b)
    pt_c_op = vdiff(base_bottom, vec_c)
    return [
        (MS.P, planeParamsFromNormalAndPoint(vec_a, pt_a), 1),
        (MS.P, planeParamsFromNormalAndPoint(vec_a, pt_a_op), -1),
        (MS.P, planeParamsFromNormalAndPoint(vec_b, pt_b), 1),
        (MS.P, planeParamsFromNormalAndPoint(vec_b, pt_b_op), -1),
        (MS.P, planeParamsFromNormalAndPoint(vec_c, pt_c), 1),
        (MS.P, planeParamsFromNormalAndPoint(vec_c, pt_c_op), -1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_top), 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_bottom), -1),
    ]


def rec(params):
    '''Transform the parameters of an REC macrobody.

    :param list params: the ten/twelve MCNP parameters for ``REC``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('REC', (10, 12), params)
    base_bottom = params[0:3]
    height = params[3:6]
    vec_maj = params[6:9]
    if len(params) == 12:
        vec_min = params[9:]
        ellipse_params = [1./scal(vec_maj, vec_maj),
                          1./scal(vec_min, vec_min)] + [0.]*7 + [-1.]
    else:  # here we have 10 params in the input
        cross_prod = vect(height, vec_maj)
        vec_min = renorm(cross_prod, params[9])
        ellipse_params = [1./scal(vec_maj, vec_maj),
                          1./params[9]**2] + [0.]*7 + [-1.]
    # ellipse_params represents the parameters of the elliptic cylinder in the
    # frame where the major axis is the x axis and the cylinder axis is the z
    # axis. We transform these parameters to the lab frame. Here is the affine
    # transform:
    u_maj = renorm(vec_maj)
    u_min = renorm(vec_min)
    u_height = renorm(height)
    transform = tuple(base_bottom) + u_maj + u_min + u_height
    cyl_params = transformation_quad(ellipse_params, transform)

    base_top = vsum(base_bottom, height)

    return [
        (MS.GQ, cyl_params, 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_top), 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_bottom), -1),
    ]


def trc(params):
    '''Transform the parameters of a TRC macrobody.

    :param list params: the fifteen MCNP parameters for ``TRC``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('TRC', 8, params)
    base_bottom = params[0:3]
    height = params[3:6]
    rad0, rad1 = params[6:]
    base_top = vsum(base_bottom, height)
    dist_to_apex = rad0/(rad0-rad1)
    apex = vsum(base_bottom, rescale(dist_to_apex, height))
    tan_aperture = math.fabs(rad1-rad0)/mag(height)
    u_height = renorm(height)
    cone_params = apex + (tan_aperture,) + u_height
    return [
        (MS.K, cone_params, 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_top), 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_bottom), -1),
    ]


def ell(params):
    '''Transform the parameters of an ELL macrobody.

    An ELL is not a generic ellipsoid, but a spheroid. It can be oblate or
    prolate depending on the parameters.

    MCNP provides two possible ways to enter the parameters, depending on the
    sign of the last one. The documentation in the MCNP manual is terse and
    does not correspond to what the code does. For instance, the surfaces

        ELL 0 0 -2  0 0 2   6
        ELL 0 0  0  0 0 3  -2

    are claimed to be equivalent, but they are not. I am not sure if the bug is
    in the code, the documentation or both. Anyway, the converter treats ELL
    like MCNP does.

    :param list params: the seven MCNP parameters for ``ELL``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('ELL', 7, params)
    last = params[-1]
    if last > 0.:
        # the parameters have the following meaning:
        # (coords of first focus) (coords of second focus) (major semi-axis)
        # \_____________________/ \______________________/        ^
        #        3 params               3 params               1 param
        focus1 = params[0:3]
        focus2 = params[3:6]
        center = rescale(0.5, vsum(focus1, focus2))
        focus1_rel = vdiff(focus1, center)
        vec_a = renorm(focus1_rel, last)
        # The following formula makes no sense. It was found by trial and error
        # and was verified to be correct by testing. The correct formula (if
        # focus1 and focus2 really represented foci) would be
        #   min_axis2 = last**2 - mag2(focus1_rel)
        min_axis2 = last**2 - (last - mag(focus1_rel))**2
    else:
        # the parameters have the following meaning:
        # (coords of center) (maj axis vector) (minor semi-axis)
        # \________________/ \_______________/        ^
        #      3 params           3 params         1 param
        center = tuple(params[0:3])
        vec_a = tuple(params[3:6])
        min_axis2 = last**2

    u_a = renorm(vec_a)
    if math.fabs(1. - math.fabs(u_a[0])) > 1e-3:
        u_b = renorm(vdiff((1, 0, 0), rescale(u_a[0], u_a)))
    elif math.fabs(1. - math.fabs(u_a[1])) > 1e-3:
        u_b = renorm(vdiff((0, 1, 0), rescale(u_a[1], u_a)))
    else:
        u_b = renorm(vdiff((0, 0, 1), rescale(u_a[2], u_a)))
    u_c = vect(u_a, u_b)
    quad_params = [1./mag2(vec_a), 1./min_axis2, 1/min_axis2] + [0]*6 + [-1.]
    transform = center + u_a + u_b + u_c
    ell_params = transformation_quad(quad_params, transform)

    return [(MS.GQ, ell_params, 1)]


def wed(params):
    '''Transform the parameters of a WED macrobody.

    :param list params: the twelve MCNP parameters for ``WED``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('WED', 12, params)
    base_bottom = params[0:3]
    vec_a = params[3:6]
    vec_b = params[6:9]
    height = params[9:]

    base_top = vsum(base_bottom, height)
    pt_a = vsum(base_bottom, vec_a)
    pt_b = vsum(base_bottom, vec_b)
    vec_ab = vdiff(vec_a, vec_b)
    vec_c = vect(vec_ab, height)
    sign_c = 1 if mixed(vec_a, vec_b, vec_c) > 0. else -1
    return [
        (MS.P, planeParamsFromNormalAndPoint(vec_c, pt_a), sign_c),
        (MS.P, planeParamsFromNormalAndPoint(vec_a, pt_b), -1),
        (MS.P, planeParamsFromNormalAndPoint(vec_b, pt_a), -1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_top), 1),
        (MS.P, planeParamsFromNormalAndPoint(height, base_bottom), -1),
    ]


def parse_facet(facet_int):
    '''Convert an integer representing a facet into a tuple of its elements.

    Polyhedron facets in the MCNP input are represented as integers. Each digit
    represents the index of a vertex. For instance, the integer 1256
    represents the facet bounded by vertices 1, 2, 5 and 6.

    This function converts the integer representation into a tuple of indices,
    which is more convenient to work with. For example:

    >>> parse_facet(1256)
    (0, 1, 4, 5)

    Note that the resulting indices are zero-based, which is more suitable for
    Python.

    Zeros are ignored:

    >>> parse_facet(5230)
    (4, 1, 2)
    >>> parse_facet(7024)
    (6, 1, 3)

    :param int facet_int: the integer representing the facets
    :returns: a tuple of indices
    :rtype: tuple(int)
    '''
    indices = []
    while facet_int != 0:
        facet_int, digit = divmod(facet_int, 10)
        facet_int, digit = int(facet_int), int(digit)
        if digit != 0:
            indices.append(digit - 1)
    return tuple(reversed(indices))


def arb(params):
    '''Transform the parameters of a ARB macrobody.

    :param list params: the thirty (!) MCNP parameters for ``ARB``
    :returns: see :func:`box`
    :rtype: list((ESurfaceTypeMCNP, list(float), int))
    '''
    check_params_length('ARB', 30, params)
    vertices = [tuple(params[3*i:3*i+3]) for i in range(8)]
    facets = [tup for tup in (parse_facet(param) for param in params[24:])
              if tup]
    n_vertices = len(set(i for facet in facets for i in facet))
    vertices = vertices[:n_vertices]

    # Even though the documentation does not mention this, it seems that MCNP
    # does not allow concave polyhedra. We use this fact to orient the planes
    # that bound the polyhedron. Specifically, we compute the centroid of the
    # vertices (which is guaranteed to lie inside the polyhedron because it is
    # convex) and we orient the normal to each plane in such a way that the
    # centroid lies on the negative side.
    centroid = rescale(1./n_vertices, vsum(*vertices))

    planes = []
    for facet in facets:
        pts = list(vertices[i] for i in facet[:3])
        plane_params = planeParamsFromPoints(*pts)
        dist = vdiff(centroid, vertices[facet[0]])
        if scal(dist, plane_params[:3]) > 0:
            plane_params = tuple(-par for par in plane_params)
        planes.append((MS.P, plane_params, 1))
    return planes

"""
Prepare parameters for creatiing surfaces in CAD.

Each function gets as argument the ist of parameters of the correspondent MCNP
surface card.  returned is a tuples describing frame, set of parameters and the
point 'below' the surface.

Transformation can be applied to the result of that functions.

Point to identify the negative-sense part must be inside the world. Since the
size of the world has no influence to CAD generation time, it can be set
arbitrarily large. For example, to ensure that all 'below'-points for particular
surface are inside the world. In this case, definition of the 'below'-points is
much more simple.

The length of the rasius-vector to the most extending 'below'-point in the model
defines the world's radius. The center of the world is at the coordinate origin.

The world's center can be improved by searching min/max values of x, y and z
used in definition of the MCNP surfaces (similar to definition of the source for
volume calculations in numjuggler).

"""

from .transforms import transform_point, transform_vector
from math import atan

# module main entry. This is a dictionary of functions that take MCNP surface
# parameters and return parameters needed to build CAD surface.
mcnp2cad = {}

# Offset to define a point 'below' a surface
_offset = 0


def _normal(x, y, z):
    """
    return arbitrary normal to (x, y, z)
    """
    if x != 0:
        a = y
        b = -x
        c = 0
    elif y != 0:
        a = 0
        b = z
        c = -y
    else:
        a = -z
        b = 0
        c = x
    check1 = a*x + b*y + c*z
    check2 = _norm(a, b, c)
    if check1 != 0 or check2 == 0:
        print(x, y, z)
        print(a, b, c)
        print(check1, check2)
        raise ValueError('Normal vector not normal or zero')
    return a, b, c


def _shift(x, y, z, A, B, C, d):
    """
    Shift point p=(x, y, z) along n=(A, B, C) to distance d.

    It is assumed that |n| = 1. In many cases I define coordinates of n manually
    and thus know in advance that they are normalized. Do not computing
    normalization here helps to save this computation for these case.
    """
    xx = x + A*d
    yy = y + B*d
    zz = z + C*d
    return (xx, yy, zz)


def _norm2(x, y, z):
    return x**2 + y**2 + z**2


def _norm(x, y, z):
    return _norm2(x, y, z)**0.5


def _sphere(x, y, z, R):
    x = x
    y = y
    z = z
    R = R
    frm = ((x, y, z), (0, 0, 1))
    srf = (R, )
    pin = (x, y, z)
    return 's', frm, srf, pin


def _plane(x, y, z, A, B, C):
    """
    Plane throught the point (x, y, z) with the normal (A, B, C). The latter
    must be normalized to have unit length.
    """
    x = x
    y = y
    z = z
    frm = ((x, y, z), (A, B, C))
    srf = ()
    pin = _shift(x, y, z, A, B, C, -_offset)
    return 'p', frm, srf, pin


def _cylinder(x, y, z, r, A, B, C):
    x = x
    y = y
    z = z
    r = r
    frm = ((x, y, z), (A, B, C))
    srf = (r, )
    pin = (x, y, z)
    return 'c', frm, srf, pin


def _cone(x, y, z, tana, A, B, C, nappe=None, log=False):
    """
    x, y, z -- cone focus coordinates,
    A, B, C -- cone axis direction, normalized to unit length
    tana -- tan of the angle

    CAD requries a point on the axis not coincident with the focus.
    """
    x = x
    y = y
    z = z
    p = _shift(x, y, z, A, B, C, _offset)
    frm = (p, (A, B, C))
    srf = (tana*_offset, atan(tana), nappe)
    if log:
        print('_cone', frm, srf, p)
    return 'k', frm, srf, p


def _torus(x, y, z, A, B, C, r1, r2, r3):
    """
    x, y, z -- coordinates of the center
    A, B, C -- normal vector to the major radius
    r1, r2  -- major and minor radii
    """
    frm = ((x, y, z), (A, B, C))
    srf = (r1, r2, r3)

    # Point inside
    n1, n2, n3 = _normal(A, B, C)
    c = r1 / _norm(n1, n2, n3)
    xi = x + c*n1
    yi = y + c*n2
    zi = z + c*n3
    pin = (xi, yi, zi)

    return 't', frm, srf, pin


def sq(params):
    frm = None, None
    srf = params.copy()
    return 'sq', frm, srf, None


def gq(params):
    frm = None, None
    srf = params.copy()

    return 'gq', frm, srf, None


################################################################################
def so(p):
    """
    Sphere defined by `so` surface.
    """
    return _sphere(0, 0, 0, p[0])


def sx(p):
    """
    Sphere defined by `sx` surface.
    """
    return _sphere(p[0], 0, 0, p[1])


def sy(p):
    """
    Sphere defined by `sy` surface.
    """
    return _sphere(0, p[0], 0, p[1])


def sz(p):
    """
    Sphere defined by `sz` surface.
    """
    return _sphere(0, 0, p[0], p[1])


def s(p):
    """
    Sphere defined by `s` surface.
    """
    return _sphere(*p)


def px(p):
    """
    Plane defined by `px` sufrace.
    """
    return _plane(p[0], 0, 0, 1, 0, 0)


def py(p):
    """
    Plane defined by `py` sufrace.
    """
    return _plane(0, p[0], 0, 0, 1, 0)


def pz(p):
    """
    Plane defined by `pz` sufrace.
    """
    return _plane(0, 0, p[0], 0, 0, 1)


def p(p):
    """
    Plane defined by `p` surface.

    The MCNP plane is defined with parameters A, B, C, D of the plane equation

        (1) Ax + By + Cz - D = 0

    From these parameters, a point lying on the plane and the normal vector to
    the plane must be found.

    Multiplying coefficients A, B, C and D by arbitrary non-zero scalar does not
    change the above equation, therefore the parameters in the MCNP surface
    card can be defined to a arbitrary non-zero constant. In the following we
    assume that the normalization holds:

        A**2 + B**2 + C**2 = 1.

    Let the plane be defined by the point p0 and the normal vector n. An
    arbitrary point p lies on the plane, if the following equation is satisfied:

        (p - p0, n) = 0,  or
        (p, n) - (p0, n) = 0

    In the rectangular coordinate system, p=(x, y, z) and the above can be
    written as

        x nx + y ny + z nz - (p0, n) = 0

    Comparing this with (1) we find n and equation to p0 in terms of the MCNP
    parameters:

        (2) n = (A, B, C)
        (3) D = (p0, n)
              = x0 A + y0 B + z0 C

    The second equation does not define p0 uniquely. Additionally, we impose
    that p0 is the closest point to the oordinate's origin, i.e. the projection
    of (0, 0, 0) onto the plane. This point is

        p0 = n/|n| d,

    where d is the distance from (0, 0, 0) to the plane. Inserting this into (3)
    we obtain expression for d:

        (p0, n) = d/|n| (n, n) = D, or

        d = D|n|/(n, n) = D/|n|

    Inserting this to the expression for p0, we obtain:

        p0 = n D/(n, n)
    """
    # normalize parameters:
    A, B, C, D = p
    c = _norm(A, B, C)
    A = A/c
    B = B/c
    C = C/c
    D = D/c
    # Point on the plane
    x, y, z = _shift(0, 0, 0, A, B, C, D)
    return _plane(x, y, z, A, B, C)


def cz(p):
    """
    Cylinder defined by `cz` surface.
    """
    return _cylinder(0, 0, 0, p[0], 0, 0, 1)


def cy(p):
    """
    Cylinder defined by `cy` surface.
    """
    return _cylinder(0, 0, 0, p[0], 0, 1, 0)


def cx(p):
    """
    Cylinder defined by `cx` surface.
    """
    return _cylinder(0, 0, 0, p[0], 1, 0, 0)


def c_z(p):
    """
    Cylinder defined by `c/z` surface.
    """
    return _cylinder(p[0], p[1], 0, p[2], 0, 0, 1)


def c_y(p):
    """
    Cylinder defined by `c/y` surface.
    """
    return _cylinder(p[0], 0, p[1], p[2], 0, 1, 0)


def c_x(p):
    """
    Cylinder defined by `c/x` surface.
    """
    return _cylinder(0, p[0], p[1], p[2], 1, 0, 0)


def cylinder(p):
    """
    Cylinder defined by `c` surface. (Not implemented in MCNP)
    """
    return _cylinder(*p)


def kz(p):
    """
    Cone defined by `kz` surface.
    """
    nappe = p[-1] if len(p) == 3 else None
    return _cone(0, 0, p[0], p[1]**0.5, 0, 0, 1, nappe)


def ky(p):
    """
    Cone defined by `ky` surface.
    """
    nappe = p[-1] if len(p) == 3 else None
    return _cone(0, p[0], 0, p[1]**0.5, 0, 1, 0, nappe)


def kx(p):
    """
    Cone defined by `kx` surface.
    """
    nappe = p[-1] if len(p) == 3 else None
    return _cone(p[0], 0, 0, p[1]**0.5, 1, 0, 0, nappe)


def k_x(p):
    """
    Cone defined by `k/x` surface.
    """
    nappe = p[-1] if len(p) == 5 else None
    return _cone(p[0], p[1], p[2], p[3]**0.5, 1, 0, 0, nappe)


def k_y(p):
    """
    Cone defined by `k/y` surface.
    """
    nappe = p[-1] if len(p) == 5 else None
    return _cone(p[0], p[1], p[2], p[3]**0.5, 0, 1, 0, nappe)


def k_z(p):
    """
    Cone defined by `k/z` surface.
    """
    nappe = p[-1] if len(p) == 5 else None
    return _cone(p[0], p[1], p[2], p[3]**0.5, 0, 0, 1, nappe)


def cone(p):
    """
    Cone defined by `k` surface. (Not implemented in MCNP)
    """
    return _cone(*p)


def tx(p):
    """"
    Torus defined by `tx` surface.
    """
    if len(p) == 5:
        x, y, z, r1, r2 = p
        return _torus(x, y, z, 1, 0, 0, r1, r2, r2)
    x, y, z, r1, r2, r3 = p
    return _torus(x, y, z, 1, 0, 0, r1, r2, r3)


def ty(p):
    """"
    Torus defined by `ty` surface.
    """
    if len(p) == 5:
        x, y, z, r1, r2 = p
        return _torus(x, y, z, 0, 1, 0, r1, r2, r2)
    x, y, z, r1, r2, r3 = p
    return _torus(x, y, z, 0, 1, 0, r1, r2, r3)


def tz(p):
    """"
    Torus defined by `tz` surface.
    """
    if len(p) == 5:
        x, y, z, r1, r2 = p
        return _torus(x, y, z, 0, 0, 1, r1, r2, r2)
    x, y, z, r1, r2, r3 = p
    return _torus(x, y, z, 0, 0, 1, r1, r2, r3)


def xx(p):
    """
    Surface defined by `x` surface.
    """
    # The meaning depends on length of p and their relative position.
    if len(p) == 2:
        # only one pair is given. This is a px plane
        return px(p)
    elif len(p) == 4:
        # Two points are given. This can be a px plane, a cx cylinder or a kx
        # cone.
        if p[0] == p[2]:
            # this is a plane
            return px(p)
        elif p[1] == p[3]:
            # this is a cylinder
            return cx((p[1], ))
        else:
            # this is a cone
            tana = (p[1] - p[3]) / (p[0] - p[2])  # half-angle tan
            x0 = p[0] - p[1]/tana
            nappe = 1 if x0 < p[0] else -1
            return _cone(x0, 0, 0, abs(tana), 1, 0, 0, nappe)
    else:
        raise NotImplementedError('Not implemented for more than 2 pairs of '
                                  'axis-symmetric surface')


def yy(p):
    """
    Surface defined by `y` surface.
    """
    # The meaning depends on length of p and their relative position.
    if len(p) == 2:
        # only one pair is given. This is a px plane
        return py(p)
    elif len(p) == 4:
        # Two points are given. This can be a px plane, a cx cylinder or a kx
        # cone.
        if p[0] == p[2]:
            # this is a plane
            return py(p)
        elif p[1] == p[3]:
            # this is a cylinder
            return cy((p[1], ))
        else:
            # this is a cone
            tana = (p[1] - p[3]) / (p[0] - p[2])  # half-angle tan
            y0 = p[0] - p[1]/tana
            nappe = 1 if y0 < p[0] else -1
            return _cone(0, y0, 0, abs(tana), 0, 1, 0, nappe)
    else:
        raise NotImplementedError('Not implemented for more than 2 pairs of '
                                  'axis-symmetric surface')


def zz(p):
    """
    Surface defined by `z` surface.
    """
    # The meaning depends on length of p and their relative position.
    if len(p) == 2:
        # only one pair is given. This is a px plane
        return pz(p)
    elif len(p) == 4:
        # Two points are given. This can be a px plane, a cx cylinder or a kx
        # cone.
        if p[0] == p[2]:
            # this is a plane
            return pz(p)
        elif p[1] == p[3]:
            # this is a cylinder
            return cz((p[1], ))
        else:
            # this is a cone
            tana = (p[1] - p[3]) / (p[0] - p[2])  # half-angle tan
            z0 = p[0] - p[1]/tana
            nappe = 1 if z0 < p[0] else -1
            return _cone(0, 0, z0, abs(tana), 0, 0, 1, nappe)
    else:
        raise NotImplementedError('Not implemented for more than 2 pairs of '
                                  'axis-symmetric surface')


mcnp2cad['so'] = so
mcnp2cad['sx'] = sx
mcnp2cad['sy'] = sy
mcnp2cad['sz'] = sz
mcnp2cad['s'] = s
mcnp2cad['px'] = px
mcnp2cad['py'] = py
mcnp2cad['pz'] = pz
mcnp2cad['p'] = p
mcnp2cad['cx'] = cx
mcnp2cad['cy'] = cy
mcnp2cad['cz'] = cz
mcnp2cad['c/x'] = c_x
mcnp2cad['c/y'] = c_y
mcnp2cad['c/z'] = c_z
mcnp2cad['c'] = cylinder
mcnp2cad['kx'] = kx
mcnp2cad['ky'] = ky
mcnp2cad['kz'] = kz
mcnp2cad['k/x'] = k_x
mcnp2cad['k/y'] = k_y
mcnp2cad['k/z'] = k_z
mcnp2cad['k'] = cone
mcnp2cad['tx'] = tx
mcnp2cad['ty'] = ty
mcnp2cad['tz'] = tz
mcnp2cad['x'] = xx
mcnp2cad['z'] = zz
mcnp2cad['sq'] = sq
mcnp2cad['gq'] = gq


def apply_transform(frm, pin, tr):
    """
    Return transformed frame frm and point pin according to transformation tr
    """
    frmp = transform_frame(frm)
    pinp = transform_point(pin, tr)
    return frmp, pinp


def transform_frame(frm, tr):
    """
    Return transformed frame frm according to transformation tr
    """
    p, v = frm
    pp = transform_point(p, tr)
    vp = transform_vector(v, tr)
    return pp, vp


def translate(surfaces, transform):
    """
    Return a dictionary of surfaces, suitable for passing to CAD.
    """
    res = surfaces.__class__()  # surfaces can be an OrderedDict
    for k, v in list(surfaces.items()):
        bc, tr, stype, pl = v
        t, f, s, p = mcnp2cad[stype](pl)
        if tr:
            trpl = transform[int(tr)]
            f, p = apply_transform(f, p, trpl)
        res[k] = t, f, s, p
    return res


def get_dimensions(surfaces):
    return 10.0


def extract_intersections():
    """
    when intersecting surfaces in SC, some of points/curves appear
    to be far from the original geometry. The idea is to represent arbitrary
    cells in the form (S1 S2 S3 ...) : (S4 S5 ...) : ... , i.e. as union of
    intersections. And search for points/curves only within each intersection
    expression.
    """
    return

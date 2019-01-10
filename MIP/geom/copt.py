"""
Finding a bounding box of a cell described by intersections is a
optimization problem with constraints (6 problems with the same
inequality conditions and the objective funtion projecting to X, Y,
and Z-axis.
"""

from scipy.optimize import minimize
from numpy import array


# Example for a finite cylinder, bounded by 1 cylinder surface and two planes.
def neg(f):
    """
    Decorator for "below" the surface.
    """
    def r(*a, **kwa):
        return -1.0 * f(*a, **kwa)
    return r


def cx5(r):
    """
    Cylinder cx 5
    """
    x, y, z = r
    return y**2 + z**2 - 25


def cx5_jac(r):
    """
    Jacobian of the cylinder
    """
    x, y, z = r
    dfdx = 0
    dfdy = 2*y
    dfdz = 2*z
    return array((dfdx, dfdy, dfdz))


def cz3(r):
    """
    Cylinder cz 3
    """
    x, y, z = r
    return x**2 + y**2 - 9


def cz3_jac(r):
    """
    Jacobian of the cylinder
    """
    x, y, z = r
    dfdx = 2*x
    dfdy = 2*y
    dfdz = 0
    return array((dfdx, dfdy, dfdz))


def px0(r):
    """
    Plane px 0
    """
    x, y, z = r
    return x


def px0_jac(r):
    return array((1, 0, 0))


def px7(r):
    """
    Plane px 7
    """
    x, y, z = r
    return x - 7


def px7_jac(r):
    return array((1, 0, 0))


con1 = ({'type': 'ineq',
         'fun': neg(cx5),
         'jac': neg(cx5_jac)},
        {'type': 'ineq',
         'fun': px0,
         'jac': px0_jac},
        {'type': 'ineq',
         'fun': neg(px7),
         'jac': neg(px7_jac)})


con2 = ({'type': 'ineq',
         'fun': neg(cx5),
         'jac': neg(cx5_jac)},
        {'type': 'ineq',
         'fun': neg(cz3),
         'jac': neg(cz3_jac)})


def o(r, s=1.0, i=0):
    return r[i]*s


def o_jac(r, s=1.0, i=0):
    a = array((0.0, 0.0, 0.0))
    a[i] = s
    return a


ddir = {'x': 0,
        'y': 1,
        'z': 2}

dopt = {'min':  1,
        'max': -1}

# Find xmin and xmax
for cons in (con1, con2):
    print('Cell', cons)
    for dn, di in sorted(ddir.items()):
        print(dn)
        for on, oi in sorted(dopt.items()):
            r = minimize(o,                 # objective
                         (0, 0, 0),         # initial guess
                         args=(oi, di),     # find min (1) or max (-1)
                         jac=o_jac,         # Objective jacobian
                         constraints=cons,  # constraints
                         )
            print(on, r.x[di])
            print(r.success)
            print(r.message)

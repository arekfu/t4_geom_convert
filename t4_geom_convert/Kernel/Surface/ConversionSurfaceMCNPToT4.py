# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
'''
from math import pi, fabs
from collections import OrderedDict

from ..FileHandlers.Parser.ParseMCNPSurface import parseMCNPSurface
from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS
from .ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from .SurfaceT4 import SurfaceT4
from .SurfaceCollection import SurfaceCollection


class SurfaceConversionError(Exception):
    '''An error in surface conversion.'''


def conversionSurfaceMCNPToT4(mcnp_parser):
    '''
    :brief: method which convert MCNP surface and constructing the
    dictionary of Surface T4
    '''
    dic_surface_t4 = OrderedDict()
    dic_surface_mcnp = parseMCNPSurface(mcnp_parser)
    for key, val in dic_surface_mcnp.items():
        surf_colls = []
        for surf, side in val:
            try:
                surf_coll = conversion_surface_params(key, surf)
            except SurfaceConversionError as err:
                msg = '{} (while converting surface {})'.format(err, key)
                raise SurfaceConversionError(msg) from None
            surf_colls.append((surf_coll, side))
        dic_surface_t4[key] = SurfaceCollection.join(surf_colls)
    return dic_surface_t4, dic_surface_mcnp


def conversion_surface_params(key, val):
    '''Convert the MCNP surface described by `val` into a TRIPOLI-4 surface.'''
    if val.type_surface in (MS.K_X, MS.K_Y, MS.K_Z, MS.KX, MS.KY, MS.KZ, MS.K):
        return convert_cone(key, val)

    if val.type_surface in (MS.P, MS.PX, MS.PY, MS.PZ):
        type_surface, param = convert_plane(val)
    elif val.type_surface in (MS.C_X, MS.C_Y, MS.C_Z, MS.CX, MS.CY, MS.CZ,
                              MS.C):
        type_surface, param = convert_cylinder(val)
    elif val.type_surface in (MS.SO, MS.S, MS.SX, MS.SY, MS.SZ):
        type_surface, param = convert_sphere(val)
    elif val.type_surface == MS.GQ:
        type_surface, param = convert_quadric(val)
    elif val.type_surface in (MS.TX, MS.TY, MS.TZ, MS.T):
        type_surface, param = convert_torus(val)
    else:
        msg = 'Unrecognized surface type: {}'.format(val.type_surface)
        raise SurfaceConversionError(msg)

    surf = SurfaceT4(type_surface, param)
    return SurfaceCollection([(surf, 1)])


def convert_plane(val):
    '''Convert the parameters for planes.'''
    tuple_param = val.param_surface
    p_x, p_y, p_z = tuple_param[0]
    u_x, u_y, u_z = tuple_param[1]
    pos = -(u_x*p_x + u_y*p_y + u_z*p_z)
    if u_x == 0. and u_y == 0. and u_z > 0.:
        type_surface = T4S.PLANEZ
        param = [-pos/u_z]
    elif u_y == 0. and u_z == 0. and u_x > 0.:
        type_surface = T4S.PLANEX
        param = [-pos/u_x]
    elif u_z == 0. and u_x == 0. and u_y > 0.:
        type_surface = T4S.PLANEY
        param = [-pos/u_y]
    else:
        type_surface = T4S.PLANE
        param = [u_x, u_y, u_z, pos]
    return type_surface, param


def convert_cylinder(val):
    '''Convert the parameters for cylinders.'''
    tuple_param = val.param_surface
    p_x, p_y, p_z = tuple_param[0]
    u_x, u_y, u_z = tuple_param[1]
    radius = val.compl_param[0]
    if u_x == 0 and u_y == 0:
        type_surface = T4S.CYLZ
        param = [p_x, p_y, radius]
    elif u_y == 0 and u_z == 0:
        type_surface = T4S.CYLX
        param = [p_y, p_z, radius]
    elif u_z == 0 and u_x == 0:
        type_surface = T4S.CYLY
        param = [p_x, p_z, radius]
    else:
        param = [p_x, p_y, p_z, radius, u_x, u_y, u_z]
        type_surface = T4S.CYL
    return type_surface, param


def convert_sphere(val):
    '''Convert the parameters for spheres.'''
    tuple_param = val.param_surface
    p_x, p_y, p_z = tuple_param[0]
    radius = val.compl_param[0]
    type_surface = T4S.SPHERE
    param = [p_x, p_y, p_z, radius]
    return type_surface, param


def convert_quadric(val):
    '''Convert the parameters for a quadric.'''
    return T4S.QUAD, val.compl_param


def convert_torus(val):
    '''Convert the parameters for tori.'''
    tuple_param = val.param_surface
    p_x, p_y, p_z = tuple_param[0]
    u_x, u_y, u_z = tuple_param[1]
    if fabs(u_x) > 0.99:
        type_surface = T4S.TORUSX
    elif fabs(u_y) > 0.99:
        type_surface = T4S.TORUSY
    elif fabs(u_z) > 0.99:
        type_surface = T4S.TORUSZ
    else:
        msg = ('Cannot convert TORUS with generic axis: ({}, {}, {})'
               .format(u_x, u_y, u_z))
        raise SurfaceConversionError(msg)
    param = [p_x, p_y, p_z] + list(val.compl_param)
    return type_surface, param


def convert_cone(key, val):
    '''Convert the parameters for cones.'''
    p_x, p_y, p_z = val.param_surface[0]
    u_x, u_y, u_z = val.param_surface[1]
    theta = 180.*val.compl_param[1]/pi
    if u_x == 0. and u_y == 0.:
        type_surface = T4S.CONEZ
        param = [p_x, p_y, p_z, theta]
    elif u_y == 0. and u_z == 0.:
        type_surface = T4S.CONEX
        param = [p_x, p_y, p_z, theta]
    elif u_z == 0. and u_x == 0.:
        type_surface = T4S.CONEY
        param = [p_x, p_y, p_z, theta]
    else:
        type_surface = T4S.CONE
        param = [p_x, p_y, p_z, theta, u_x, u_y, u_z]
    cone = SurfaceT4(type_surface, param)

    nappe = val.compl_param[2] if len(val.compl_param) == 3 else None
    if nappe is None or nappe == 0:
        return SurfaceCollection([(cone, 1)])

    pos = -(u_x*p_x + u_y*p_y + u_z*p_z)
    if u_x == 0 and u_y == 0:
        type_surface = T4S.PLANEZ
        param = [-pos/u_z]
    elif u_y == 0 and u_z == 0:
        type_surface = T4S.PLANEX
        param = [-pos/u_x]
    elif u_z == 0 and u_x == 0:
        type_surface = T4S.PLANEY
        param = [-pos/u_y]
    else:
        type_surface = T4S.PLANE
        param = [u_x, u_y, u_z, pos]
    plane = SurfaceT4(type_surface, param,
                      ['aux plane for cone {}'.format(key)])
    return SurfaceCollection([(cone, 1), (plane, -int(nappe))])

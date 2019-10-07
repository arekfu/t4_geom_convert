# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
'''
from math import atan, pi, sqrt, fabs
from collections import OrderedDict

from .CDictSurfaceMCNP import CDictSurfaceMCNP
from .CDictSurfaceT4 import CDictSurfaceT4
from .DTypeConversion import dict_conversionSurfaceType
from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS
from .ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from .CSurfaceT4 import CSurfaceT4
from .CSurfaceCollection import CSurfaceCollection
from ..VectUtils import planeParamsFromPoints


def conversionSurfaceMCNPToT4(mcnpParser):
    '''
    :brief: method which convert MCNP surface and constructing the
    dictionary of Surface T4
    '''
    dic_SurfaceT4 = OrderedDict()
    obj_T4 = CDictSurfaceT4(dic_SurfaceT4)
    dic_surface_mcnp = CDictSurfaceMCNP(mcnpParser).d_surfaceMCNP
    for key, val in dic_surface_mcnp.items():
        try:
            surfacesT4 = conversionSurfaceParams(key, val)
            # surfacesT4 = _surfaceParametresConversion(key, val)
        except:
            print(key, 'Parameters of this surface do not comply')
            raise
        obj_T4[key] = surfacesT4
    return dic_SurfaceT4, dic_surface_mcnp


def conversionSurfaceParams(key, val):
    if val.typeSurface in (MS.P, MS.PX, MS.PY, MS.PZ):
        tuple_param = val.paramSurface
        x, y, z = tuple_param[0]
        ux, uy, uz = tuple_param[1]
        pos = -(ux*x + uy*y + uz*z)
        if ux == 0. and uy == 0. and uz > 0.:
            type_surface = T4S.PLANEZ
            param = [-pos/uz]
        elif uy == 0. and uz == 0. and ux > 0.:
            type_surface = T4S.PLANEX
            param = [-pos/ux]
        elif uz == 0. and ux == 0. and uy > 0.:
            type_surface = T4S.PLANEY
            param = [-pos/uy]
        else:
            type_surface = T4S.PLANE
            param = [ux, uy, uz, pos]
    elif val.typeSurface in (MS.C_X, MS.C_Y, MS.C_Z, MS.CX, MS.CY, MS.CZ,
                             MS.C):
        tuple_param = val.paramSurface
        x, y, z = tuple_param[0]
        ux, uy, uz = tuple_param[1]
        r = val.complParam[0]
        if ux == 0 and uy == 0:
            type_surface = T4S.CYLZ
            param = [x, y, r]
        elif uy == 0 and uz == 0:
            type_surface = T4S.CYLX
            param = [y, z, r]
        elif uz == 0 and ux == 0:
            type_surface = T4S.CYLY
            param = [x, z, r]
        else:
            param = [x, y, z, r, ux, uy, uz]
            type_surface = T4S.CYL
    elif val.typeSurface in (MS.SO, MS.S, MS.SX, MS.SY, MS.SZ):
        tuple_param = val.paramSurface
        x, y, z = tuple_param[0]
        r = val.complParam[0]
        type_surface = T4S.SPHERE
        param = [x, y, z, r]
    elif val.typeSurface in (MS.K_X, MS.K_Y, MS.K_Z, MS.KX, MS.KY, MS.KZ,
                             MS.K):
        tuple_param = val.paramSurface
        x, y, z = tuple_param[0]
        ux, uy, uz = tuple_param[1]
        teta = 180.*val.complParam[1]/pi
        if ux == 0. and uy == 0.:
            type_surface = T4S.CONEZ
            param = [x, y, z, teta]
        elif uy == 0. and uz == 0.:
            type_surface = T4S.CONEX
            param = [x, y, z, teta]
        elif uz == 0. and ux == 0.:
            type_surface = T4S.CONEY
            param = [x, y, z, teta]
        else:
            type_surface = T4S.CONE
            param = [x, y, z, teta, ux, uy, uz]
        cone = CSurfaceT4(type_surface, param)

        nappe = val.complParam[2] if len(val.complParam) == 3 else None
        if nappe is None or nappe == 0:
            return CSurfaceCollection(cone)
        pos = -(ux*x + uy*y + uz*z)

        if ux == 0 and uy == 0:
            type_surface = T4S.PLANEZ
            param = [-pos/uz]
            side = int(nappe) if uz > 0. else -int(nappe)
        elif uy == 0 and uz == 0:
            type_surface = T4S.PLANEX
            param = [-pos/ux]
            side = int(nappe) if ux > 0. else -int(nappe)
        elif uz == 0 and ux == 0:
            type_surface = T4S.PLANEY
            param = [-pos/uy]
            side = int(nappe) if uy > 0. else -int(nappe)
        else:
            typePlane = T4S.PLANE
            paramPlane = [ux, uy, uz, pos]
            side = int(nappe)
        plane = CSurfaceT4(type_surface, param,
                           ['aux plane for cone {}'.format(key)])
        return CSurfaceCollection(cone, fixed=[(plane, side)])
    elif val.typeSurface == MS.GQ:
        type_surface = T4S.QUAD
        param = val.complParam
    elif val.typeSurface in (MS.TX, MS.TY, MS.TZ, MS.T):
        tuple_param = val.paramSurface
        x, y, z = tuple_param[0]
        ux, uy, uz = tuple_param[1]
        if fabs(ux)> 0.99:
            type_surface = T4S.TORUSX
        elif fabs(uy)> 0.99:
            type_surface = T4S.TORUSY
        elif fabs(uz)> 0.99:
            type_surface = T4S.TORUSZ
        else:
            raise ValueError('Cannot convert TORUS with generic axis: %s'%unitary_vector)
        param = [x, y, z] + list(val.complParam)
    else:
        raise ValueError('Unrecognized surface type: {}'.format(val.typeSurface))


    surf = CSurfaceT4(type_surface, param)
    return CSurfaceCollection(surf)

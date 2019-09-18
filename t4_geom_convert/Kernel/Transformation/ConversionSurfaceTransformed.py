# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
'''
from .SurfaceTransformed import surfaceTransformed
from ..Surface.ESurfaceTypeT4 import ESurfaceTypeT4Eng
from ..Surface.CSurfaceT4 import CSurfaceT4
from ..Surface.CSurfaceCollection import CSurfaceCollection
import math
from collections import OrderedDict
from math import pi


def conversionSurfaceTransformed(mcnpParser):
    dic_SurfaceT4Tr = OrderedDict()
    dicSurfaceTransformed = surfaceTransformed(mcnpParser)
    for k, val in dicSurfaceTransformed.items():
        dic_SurfaceT4Tr[k] = conversionSurfaceParams(val)

    return dic_SurfaceT4Tr, dicSurfaceTransformed


def conversionSurfaceParams(val):
    if val.typeSurface == 'p':
        tuple_param = val.paramSurface
        point = tuple_param[0]
        unitary_vector = tuple_param[1]
        x, y, z = point
        A, B, C = unitary_vector
        D = -(A*x + B*y + C*z)
        param = [A,B,C,D]
        type_surface = ESurfaceTypeT4Eng.PLANE
    if val.typeSurface == 'c':
        tuple_param = val.paramSurface
        point = tuple_param[0]
        unitary_vector = tuple_param[1]
        x,y,z = point
        ux, uy, uz = unitary_vector
        r = tuple_param[2][0]
        param = [x, y, z, r, ux, uy, uz]
        type_surface = ESurfaceTypeT4Eng.CYL
    if val.typeSurface == 's':
        tuple_param = val.paramSurface
        point = tuple_param[0]
        r = tuple_param[2][0]
        x,y,z = point
        param = [x, y, z, r]
        type_surface = ESurfaceTypeT4Eng.SPHERE
    if val.typeSurface == 'k':
        tuple_param = val.paramSurface
        point = tuple_param[0]
        x, y, z = point
        unitary_vector = tuple_param[1]
        teta = 180.*tuple_param[2][1]/pi
        ux, uy, uz = unitary_vector
        param = [x, y, z, teta, ux, uy, uz]
        type_surface = ESurfaceTypeT4Eng.CONE
        nappe = tuple_param[2][2]
        cone = CSurfaceT4(type_surface, param)
        if nappe is None or nappe == 0:
            return CSurfaceCollection(cone)
        D = -(ux*x + uy*y + uz*z)
        paramPlane = [ux,uy,uz,D]
        typePlane = ESurfaceTypeT4Eng.PLANE
        plane = CSurfaceT4(typePlane, paramPlane)
        side = int(nappe)
        return CSurfaceCollection(cone, fixed=[(plane, side)])
    if val.typeSurface == 'gq':
        type_surface = ESurfaceTypeT4Eng.QUAD
        param = val.paramSurface
    if val.typeSurface =='t':
        tuple_param = val.paramSurface
        point = tuple_param[0]
        unitary_vector = tuple_param[1]
        x,y,z = point
        ux, uy, uz = unitary_vector
        r1 = tuple_param[2][0]
        r2 = tuple_param[2][1]
        if math.fabs(ux)> 0.99:
            type_surface = ESurfaceTypeT4Eng.TORUSX
        elif math.fabs(uy)> 0.99:
            type_surface = ESurfaceTypeT4Eng.TORUSY
        elif math.fabs(uz)> 0.99:
            type_surface = ESurfaceTypeT4Eng.TORUSZ
        else:
            raise ValueError('Cannot convert TORUS with generic axis: %s'%unitary_vector)
        param = [x,y,z,r1, r2, r2]

    surf = CSurfaceT4(type_surface, param)
    return CSurfaceCollection(surf)

# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
:file : CConversionSurfaceTransformed.py
'''
from ..Transformation.CDictSurfaceTransformed import CDictSurfaceTransformed
from ..Surface.ESurfaceTypeT4 import ESurfaceTypeT4Eng
from ..Surface.CSurfaceT4 import CSurfaceT4
from ..Surface.CSurfaceCollection import CSurfaceCollection
import math
from collections import OrderedDict
from math import pi

class CConversionSurfaceTransformed(object):
    '''
    :brief: Class containing function to transform surface and volume
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def m_conversionSurfaceTransformed(self):
        dic_SurfaceT4Tr = OrderedDict()
        dicSurfaceTransformed = CDictSurfaceTransformed().m_surfaceTransformed()
        for k, val in dicSurfaceTransformed.items():
            #print('transformation', k)
            dic_SurfaceT4Tr[k] = self.m_conversion(val)

        return dic_SurfaceT4Tr, dicSurfaceTransformed

    def m_conversion(self, val):
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
            if nappe is None:
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
            #print('je suis T')
            tuple_param = val.paramSurface
            point = tuple_param[0]
            unitary_vector = tuple_param[1]
            x,y,z = point
            ux, uy, uz = unitary_vector
            r1 = tuple_param[2][0]
            r2 = tuple_param[2][1]
            if math.fabs(ux)> 0.99:
                #print('je suis tx')
                type_surface = ESurfaceTypeT4Eng.TORUSX
            elif math.fabs(uy)> 0.99:
                #print('je suis ty')
                type_surface = ESurfaceTypeT4Eng.TORUSY
            elif math.fabs(uz)> 0.99:
                #print('je suis tz')
                type_surface = ESurfaceTypeT4Eng.TORUSZ
            else:
                raise ValueError('Cannot convert TORUS with generic axis: %s'%unitary_vector)
            param = [x,y,z,r1, r2, r2]

        surf = CSurfaceT4(type_surface, param)
        return CSurfaceCollection(surf)

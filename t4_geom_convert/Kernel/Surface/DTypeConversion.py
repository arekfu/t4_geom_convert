# -*- coding: utf-8 -*-
'''

:author: Sogeti
:data : 06 february 2019
:file : DTypeConversion.py
'''
from .ESurfaceTypeMCNP import ESurfaceTypeMCNP as e_surfaceMCNP
from .ESurfaceTypeT4 import ESurfaceTypeT4 as e_surfaceT4


'''
:brief: Python file specifying each conversion of surface type
'''


dict_conversionSurfaceType = dict()

dict_conversionSurfaceType[e_surfaceMCNP.PX] = e_surfaceT4.PLANEX
dict_conversionSurfaceType[e_surfaceMCNP.PY] = e_surfaceT4.PLANEY
dict_conversionSurfaceType[e_surfaceMCNP.PZ] = e_surfaceT4.PLANEZ
dict_conversionSurfaceType[e_surfaceMCNP.P] = e_surfaceT4.PLANE
dict_conversionSurfaceType[e_surfaceMCNP.SO] = e_surfaceT4.SPHERE
dict_conversionSurfaceType[e_surfaceMCNP.S] = e_surfaceT4.SPHERE
dict_conversionSurfaceType[e_surfaceMCNP.SX] = e_surfaceT4.SPHERE
dict_conversionSurfaceType[e_surfaceMCNP.SY] = e_surfaceT4.SPHERE
dict_conversionSurfaceType[e_surfaceMCNP.SZ] = e_surfaceT4.SPHERE
dict_conversionSurfaceType[e_surfaceMCNP.C_X] = e_surfaceT4.CYLX
dict_conversionSurfaceType[e_surfaceMCNP.C_Y] = e_surfaceT4.CYLY
dict_conversionSurfaceType[e_surfaceMCNP.C_Z] = e_surfaceT4.CYLZ
dict_conversionSurfaceType[e_surfaceMCNP.CX] = e_surfaceT4.CYLX
dict_conversionSurfaceType[e_surfaceMCNP.CY] = e_surfaceT4.CYLY
dict_conversionSurfaceType[e_surfaceMCNP.CZ] = e_surfaceT4.CYLZ
dict_conversionSurfaceType[e_surfaceMCNP.K_X] = e_surfaceT4.CONEX
dict_conversionSurfaceType[e_surfaceMCNP.K_Y] = e_surfaceT4.CONEY
dict_conversionSurfaceType[e_surfaceMCNP.K_Z] = e_surfaceT4.CONEZ
dict_conversionSurfaceType[e_surfaceMCNP.KX] = e_surfaceT4.CONEX
dict_conversionSurfaceType[e_surfaceMCNP.KY] = e_surfaceT4.CONEY
dict_conversionSurfaceType[e_surfaceMCNP.KZ] = e_surfaceT4.CONEZ
dict_conversionSurfaceType[e_surfaceMCNP.GQ] = e_surfaceT4.QUAD
dict_conversionSurfaceType[e_surfaceMCNP.TX] = e_surfaceT4.TORUSX
dict_conversionSurfaceType[e_surfaceMCNP.TY] = e_surfaceT4.TORUSY
dict_conversionSurfaceType[e_surfaceMCNP.TZ] = e_surfaceT4.TORUSZ
# SQ intentionally omitted, transformed into equivalent GQ during parsing

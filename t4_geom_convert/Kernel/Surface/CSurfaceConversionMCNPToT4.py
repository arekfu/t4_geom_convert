# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
:file : CSurfaceConversionMCNPToT4.py

.. doctest:: CIntermediateSurfaceT4
    :hide:
    >>> from CIntermediateSurfaceT4 import CIntermediateSurfaceT4
    >>> p = CSurfaceConversionMCNPToT4().m_conversionMCNPToT4()
    >>> for key,val in p.items():
    >>> print(key, val))
'''
from ..Surface.CDictSurfaceMCNP import CDictSurfaceMCNP
from ..Surface.CDictSurfaceT4 import CDictSurfaceT4
from ..Surface.DTypeConversion import dict_conversionSurfaceType
import math

class CSurfaceConversionMCNPToT4(object):
    '''
    :brief: Class transforming surface MCNP in T4
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def m_conversionMCNPToT4(self):
        '''
        :brief: method which convert MCNP surface and constructing the
        dictionary of Surface T4
        '''
        dic_SurfaceT4 = dict()
        obj_T4 = CDictSurfaceT4(dic_SurfaceT4)
        for key, val in CDictSurfaceMCNP().d_surfaceMCNP.items():
            typeSurfaceMCNP = val.typeSurface
            typeSurfaceT4 = dict_conversionSurfaceType[typeSurfaceMCNP]
            try:
                listCoefSurfaceT4 = self.m_surfaceParametresConversion(typeSurfaceMCNP,
                                                                   val.paramSurface)
            except:
                print(key, 'Parameters of this surface do not comply')
                raise
            valueT4 = (typeSurfaceT4, listCoefSurfaceT4)
            obj_T4.__setitem__(key, valueT4)
        return dic_SurfaceT4

    def m_surfaceParametresConversion(self, p_typeSurfaceMCNP, p_listeParametreMCNP):
        '''
        method which take information of the MCNP Surface and return a list of
        converted surface in T4
        '''
        listeParametreT4 = []
        if p_typeSurfaceMCNP.name == "PX" or p_typeSurfaceMCNP.name == "PY" or\
        p_typeSurfaceMCNP.name == "PZ" and len(p_listeParametreMCNP) == 1:
            listeParametreT4 = p_listeParametreMCNP
        elif p_typeSurfaceMCNP.name == "P" or p_typeSurfaceMCNP.name == "S" and\
        len(p_listeParametreMCNP) == 4:
            listeParametreT4 = p_listeParametreMCNP
        elif p_typeSurfaceMCNP.name == "C/X" or p_typeSurfaceMCNP.name == "C/Y" or\
        p_typeSurfaceMCNP.name == "C/Z"  and len(p_listeParametreMCNP) == 3:
            listeParametreT4 = p_listeParametreMCNP
        elif p_typeSurfaceMCNP.name == "GQ"  and len(p_listeParametreMCNP) == 8:
            listeParametreT4 = p_listeParametreMCNP
        elif p_typeSurfaceMCNP.name == "SO"  and len(p_listeParametreMCNP) == 1:
            listeParametreT4 = [0, 0, 0, p_listeParametreMCNP[0]]
        elif p_typeSurfaceMCNP.name == "SX"  and len(p_listeParametreMCNP) == 2:
            listeParametreT4 = [p_listeParametreMCNP[0], 0, 0, p_listeParametreMCNP[1]]
        elif p_typeSurfaceMCNP.name == "SY"  and len(p_listeParametreMCNP) == 2:
            listeParametreT4 = [0, p_listeParametreMCNP[0], 0, p_listeParametreMCNP[1]]
        elif p_typeSurfaceMCNP.name == "SZ"  and len(p_listeParametreMCNP) == 2:
            listeParametreT4 = [0, 0, p_listeParametreMCNP[0], p_listeParametreMCNP[1]]
        elif p_typeSurfaceMCNP.name == "CX" or p_typeSurfaceMCNP.name == "CY" or\
        p_typeSurfaceMCNP.name == "CZ"  and len(p_listeParametreMCNP) == 1:
            listeParametreT4 = [0, 0, p_listeParametreMCNP[0]]
        elif (p_typeSurfaceMCNP.name == "K/X"
              or p_typeSurfaceMCNP.name == "K/Y"
              or p_typeSurfaceMCNP.name == "K/Z"):
            p_atant = math.atan(math.sqrt(float(p_listeParametreMCNP[3])))
            if len(p_listeParametreMCNP) == 4:
                listeParametreT4 = [p_listeParametreMCNP[0],
                                    p_listeParametreMCNP[1],
                                    p_listeParametreMCNP[2], p_atant]
            elif len(p_listeParametreMCNP) == 5:
                listeParametreT4 = [p_listeParametreMCNP[0],
                                    p_listeParametreMCNP[1],
                                    p_listeParametreMCNP[2], p_atant,
                                    p_listeParametreMCNP[4]]
            else:
                msg = ('Unexpected number of MCNP parameters in {} surface: {}'
                       .format(p_typeSurfaceMCNP, len(p_listeParametreMCNP)))
                raise ValueError(msg)
        elif p_typeSurfaceMCNP.name == "KX":
            if len(p_listeParametreMCNP) == 2:
                p_atant = math.atan(math.sqrt(float(p_listeParametreMCNP[1])))
                listeParametreT4 = [p_listeParametreMCNP[0], 0, 0, p_atant]
            else:
                raise ValueError('Cannot handle 1-nappe KX cones (yet)')
        elif p_typeSurfaceMCNP.name == "KY":
            if len(p_listeParametreMCNP) == 2:
                p_atant = math.atan(math.sqrt(float(p_listeParametreMCNP[1])))
                listeParametreT4 = [0, p_listeParametreMCNP[0], 0, p_atant]
            else:
                raise ValueError('Cannot handle 1-nappe KY cones (yet)')
        elif p_typeSurfaceMCNP.name == "KZ":
            if len(p_listeParametreMCNP) == 2:
                p_atant = math.atan(math.sqrt(float(p_listeParametreMCNP[1])))
                listeParametreT4 = [0, 0, p_listeParametreMCNP[0], p_atant]
            else:
                raise ValueError('Cannot handle 1-nappe KZ cones (yet)')
        else:
            raise ValueError('Cannot convert MCNP surface: {} {}'
                             .format(p_typeSurfaceMCNP, p_listeParametreMCNP))

        return listeParametreT4

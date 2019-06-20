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
from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MCNPS
from ..Surface.ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from math import atan, pi, sqrt

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
            try:
                surfacesT4 = self.m_surfaceParametresConversion(val)
            except:
                print(key, 'Parameters of this surface do not comply')
                raise
            obj_T4[key] = surfacesT4
        return dic_SurfaceT4

    def m_surfaceParametresConversion(self, p_surfaceMCNP):
        '''
        method which take information of the MCNP Surface and return a list of
        converted surface in T4
        '''
        typeSurfaceMCNP = p_surfaceMCNP.typeSurface
        listeParametreMCNP = p_surfaceMCNP.paramSurface
        
        if typeSurfaceMCNP not in (MCNPS.X, MCNPS.Y, MCNPS.Z):
            typeSurfaceT4 = dict_conversionSurfaceType[typeSurfaceMCNP]

        # First handle cones, which are a bit of a special case due to the fact
        # that they can have an extra +-1 parameter to indicate one-nappe
        # cones. Since one-nappe cones are not implemented in TRIPOLI-4, we
        # have to emulate them using a two-nappe cone and a plane. We return
        # the TRIPOLI-4 two-nappe cone, plus a pair consisting of the TRIPOLI-4
        # plane and the side of the plane which should be used, regardless of
        # which side of the cone appears in the cell definition.
        if typeSurfaceMCNP == MCNPS.KX:
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[1])))/pi
            listeParametreT4 = [listeParametreMCNP[0], 0, 0, p_atant]
            coneT4 = (typeSurfaceT4, listeParametreT4)
            if len(listeParametreMCNP) == 2:
                return [coneT4]
            if len(listeParametreMCNP) == 3:
                side = int(listeParametreMCNP[-1])
                planeT4 = (T4S.PLANEX, [listeParametreMCNP[0]])
                return [coneT4, (planeT4, side)]
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP == MCNPS.KY:
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[1])))/pi
            listeParametreT4 = [0, listeParametreMCNP[0], 0, p_atant]
            coneT4 = (typeSurfaceT4, listeParametreT4)
            if len(listeParametreMCNP) == 2:
                return [coneT4]
            if len(listeParametreMCNP) == 3:
                side = int(listeParametreMCNP[-1])
                planeT4 = (T4S.PLANEY, [listeParametreMCNP[0]])
                return [coneT4, (planeT4, side)]
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP == MCNPS.KZ:
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[1])))/pi
            listeParametreT4 = [0, 0, listeParametreMCNP[0], p_atant]
            coneT4 = (typeSurfaceT4, listeParametreT4)
            if len(listeParametreMCNP) == 2:
                return [coneT4]
            if len(listeParametreMCNP) == 3:
                side = int(listeParametreMCNP[-1])
                planeT4 = (T4S.PLANEZ, [listeParametreMCNP[0]])
                return [coneT4, (planeT4, side)]
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP in (MCNPS.K_X, MCNPS.K_Y, MCNPS.K_Z):
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[3])))/pi
            listeParametreT4 = [listeParametreMCNP[0],
                                listeParametreMCNP[1],
                                listeParametreMCNP[2], p_atant]
            coneT4 = (typeSurfaceT4, listeParametreT4)
            if len(listeParametreMCNP) == 4:
                return [coneT4]
            if len(listeParametreMCNP) == 5:
                side = int(listeParametreMCNP[-1])
                if typeSurfaceMCNP == MCNPS.K_X:
                    planeT4 = (T4S.PLANEX, [listeParametreMCNP[0]])
                elif typeSurfaceMCNP == MCNPS.K_Y:
                    planeT4 = (T4S.PLANEY, [listeParametreMCNP[1]])
                elif typeSurfaceMCNP == MCNPS.K_Z:
                    planeT4 = (T4S.PLANEZ, [listeParametreMCNP[2]])
                return [coneT4, (planeT4, side)]
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP == MCNPS.X:
            # The meaning depends on lentgth of p and their relative position.
            if len(listeParametreMCNP) == 2:
                # only one pair is given. This is a px plane
                listeParametreT4 = [listeParametreMCNP[0]]
                typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PX]
                return [(typeSurfaceT4, listeParametreT4)]
            elif len(listeParametreMCNP) == 4:
                # Two points are given. This can be a px plane, a cx cylinder or a kx
                # cone.
                if listeParametreMCNP[0] == listeParametreMCNP[2]:
                    # this is a plane
                    listeParametreT4 = [listeParametreMCNP[0]]
                    typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PX]
                    return [(typeSurfaceT4, listeParametreT4)]
                elif listeParametreMCNP[1] == listeParametreMCNP[3]:
                    # this is a cylinder
                    listeParametreT4 = [0, 0, listeParametreMCNP[1]]
                    typeSurfaceT4 = T4S.CYLX
                    return [(typeSurfaceT4, listeParametreT4)]
                else:
                    # this is a cone
                    typeSurfaceT4 = T4S.CONEX
                    tana = (listeParametreMCNP[1] - listeParametreMCNP[3])\
                     / (listeParametreMCNP[0] - listeParametreMCNP[2])  # half-angle tan
                    x0 = listeParametreMCNP[0] - listeParametreMCNP[1]/tana
                    a = atan(tana)
                    listeParametreT4 = [x0, 0, 0, abs(a)]
                    return [(typeSurfaceT4, listeParametreT4)]
        elif typeSurfaceMCNP == MCNPS.Y:
            # The meaning depends on lentgth of p and their relative position.
            if len(listeParametreMCNP) == 2:
                # only one pair is given. This is a py plane
                listeParametreT4 = [listeParametreMCNP[0]]
                typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PY]
                return [(typeSurfaceT4, listeParametreT4)]
            elif len(listeParametreMCNP) == 4:
                # Two points are given. This can be a py plane, a cy cylinder or a ky
                # cone.
                if listeParametreMCNP[0] == listeParametreMCNP[2]:
                    # this is a plane
                    listeParametreT4 = [listeParametreMCNP[0]]
                    typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PY]
                    return [(typeSurfaceT4, listeParametreT4)]
                elif listeParametreMCNP[1] == listeParametreMCNP[3]:
                    # this is a cylinder
                    listeParametreT4 = [0, 0, listeParametreMCNP[1]]
                    typeSurfaceT4 = T4S.CYLY
                    return [(typeSurfaceT4, listeParametreT4)]
                else:
                    # this is a cone
                    typeSurfaceT4 = T4S.CONEY
                    tana = (listeParametreMCNP[1] - listeParametreMCNP[3])\
                     / (listeParametreMCNP[0] - listeParametreMCNP[2])  # half-angle tan
                    y0 = listeParametreMCNP[0] - listeParametreMCNP[1]/tana
                    a = atan(tana)
                    listeParametreT4 = [0, y0, 0, abs(a)]
                    return [(typeSurfaceT4, listeParametreT4)]
        elif typeSurfaceMCNP == MCNPS.Z:
            if len(listeParametreMCNP) == 2:
                listeParametreT4 = [listeParametreMCNP[0]]
                typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PZ]
                return [(typeSurfaceT4, listeParametreT4)]
            elif len(listeParametreMCNP) == 4:
                # Two points are given. This can be a px plane, a cx cylinder or a kx
                # cone.
                if listeParametreMCNP[0] == listeParametreMCNP[2]:
                    # this is a plane
                    listeParametreT4 = [listeParametreMCNP[0]]
                    typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PZ]
                    return [(typeSurfaceT4, listeParametreT4)]
                elif listeParametreMCNP[1] == listeParametreMCNP[3]:
                    # this is a cylinder
                    listeParametreT4 = [0, 0, listeParametreMCNP[1]]
                    typeSurfaceT4 = T4S.CYLZ
                    return [(typeSurfaceT4, listeParametreT4)]
                else:
                    # this is a cone
                    typeSurfaceT4 = T4S.CONEZ
                    tana = (listeParametreMCNP[1] - \
                    listeParametreMCNP[3]) / (listeParametreMCNP[0] - listeParametreMCNP[2])  # half-angle tan
                    a = atan(tana)
                    z0 = listeParametreMCNP[0] - listeParametreMCNP[1]/tana
                    listeParametreT4 = [0, 0, z0, atan(a)]
                    return [(typeSurfaceT4, listeParametreT4)]

        # Not a cone, fall back to the normal treatment
        if typeSurfaceMCNP in (MCNPS.TX, MCNPS.TY, MCNPS.TZ):
            listeParametreT4 = listeParametreMCNP
        elif (typeSurfaceMCNP in (MCNPS.PX, MCNPS.PY, MCNPS.PZ)
            and len(listeParametreMCNP) == 1):
            listeParametreT4 = listeParametreMCNP
        elif (typeSurfaceMCNP in (MCNPS.P, MCNPS.S)
              and len(listeParametreMCNP) == 4):
            listeParametreT4 = listeParametreMCNP
        elif (typeSurfaceMCNP in (MCNPS.C_X, MCNPS.C_Y, MCNPS.C_Z)
              and len(listeParametreMCNP) == 3):
            listeParametreT4 = listeParametreMCNP
        elif typeSurfaceMCNP == MCNPS.GQ  and len(listeParametreMCNP) == 10:
            listeParametreT4 = listeParametreMCNP
        elif typeSurfaceMCNP == MCNPS.SO  and len(listeParametreMCNP) == 1:
            listeParametreT4 = [0, 0, 0, listeParametreMCNP[0]]
        elif typeSurfaceMCNP == MCNPS.SX  and len(listeParametreMCNP) == 2:
            listeParametreT4 = [listeParametreMCNP[0], 0, 0, listeParametreMCNP[1]]
        elif typeSurfaceMCNP == MCNPS.SY  and len(listeParametreMCNP) == 2:
            listeParametreT4 = [0, listeParametreMCNP[0], 0, listeParametreMCNP[1]]
        elif typeSurfaceMCNP == MCNPS.SZ  and len(listeParametreMCNP) == 2:
            listeParametreT4 = [0, 0, listeParametreMCNP[0], listeParametreMCNP[1]]
        elif (typeSurfaceMCNP in (MCNPS.CX, MCNPS.CY, MCNPS.CZ)
              and len(listeParametreMCNP) == 1):
            listeParametreT4 = [0, 0, listeParametreMCNP[0]]
        else:
            raise ValueError('Cannot convert MCNP surface: {} {}'
                             .format(typeSurfaceMCNP, listeParametreMCNP))

        return [(typeSurfaceT4, listeParametreT4)]

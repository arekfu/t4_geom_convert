# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
:file : CSurfaceConversionMCNPToT4.py

.. doctest:: CIntermediateSurfaceT4
    :hide:
    >>> from CIntermediateSurfaceT4 import CIntermediateSurfaceT4
    >>> p = CSurfaceConversionMCNPToT4().conversionMCNPToT4()
    >>> for key,val in p.items():
    >>> print(key, val))
'''
from .CDictSurfaceMCNP import CDictSurfaceMCNP
from .CDictSurfaceT4 import CDictSurfaceT4
from .DTypeConversion import dict_conversionSurfaceType
from .ESurfaceTypeMCNP import ESurfaceTypeMCNP as MCNPS
from .ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from .CSurfaceT4 import CSurfaceT4
from .CSurfaceCollection import CSurfaceCollection
from math import atan, pi, sqrt, fabs
from collections import OrderedDict

class CSurfaceConversionMCNPToT4(object):
    '''
    :brief: Class transforming surface MCNP in T4
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def conversionMCNPToT4(self):
        '''
        :brief: method which convert MCNP surface and constructing the
        dictionary of Surface T4
        '''
        dic_SurfaceT4 = OrderedDict()
        obj_T4 = CDictSurfaceT4(dic_SurfaceT4)
        dic_surface_mcnp = CDictSurfaceMCNP().d_surfaceMCNP
        for key, val in dic_surface_mcnp.items():
            try:
                surfacesT4 = self.surfaceParametresConversion(key, val)
            except:
                print(key, 'Parameters of this surface do not comply')
                raise
            obj_T4[key] = surfacesT4
        return dic_SurfaceT4, dic_surface_mcnp

    def surfaceParametresConversion(self, key, p_surfaceMCNP):
        '''
        method which take information of the MCNP Surface and return a list of
        converted surface in T4
        '''
        typeSurfaceMCNP = p_surfaceMCNP.typeSurface
        listeParametreMCNP = p_surfaceMCNP.paramSurface
        idorigin = p_surfaceMCNP.idorigin.copy()
        idorigin.append(key)

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
            coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                idorigin=idorigin)
            if len(listeParametreMCNP) == 2:
                return CSurfaceCollection(coneT4)
            if len(listeParametreMCNP) == 3:
                side = int(listeParametreMCNP[-1])
                plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                planeT4 = CSurfaceT4(T4S.PLANEX, [listeParametreMCNP[0]],
                                     idorigin=plane_idorigin)
                return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP == MCNPS.KY:
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[1])))/pi
            listeParametreT4 = [0, listeParametreMCNP[0], 0, p_atant]
            coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                idorigin=idorigin)
            if len(listeParametreMCNP) == 2:
                return CSurfaceCollection(coneT4)
            if len(listeParametreMCNP) == 3:
                side = int(listeParametreMCNP[-1])
                plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                planeT4 = CSurfaceT4(T4S.PLANEY, [listeParametreMCNP[0]],
                                     idorigin=plane_idorigin)
                return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP == MCNPS.KZ:
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[1])))/pi
            listeParametreT4 = [0, 0, listeParametreMCNP[0], p_atant]
            coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                idorigin=idorigin)
            if len(listeParametreMCNP) == 2:
                return CSurfaceCollection(coneT4)
            if len(listeParametreMCNP) == 3:
                side = int(listeParametreMCNP[-1])
                plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                planeT4 = CSurfaceT4(T4S.PLANEZ, [listeParametreMCNP[0]],
                                     idorigin=plane_idorigin)
                return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP in (MCNPS.K_X, MCNPS.K_Y, MCNPS.K_Z):
            p_atant = 180.*atan(sqrt(float(listeParametreMCNP[3])))/pi
            listeParametreT4 = [listeParametreMCNP[0],
                                listeParametreMCNP[1],
                                listeParametreMCNP[2], p_atant]
            coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                idorigin=idorigin)
            if len(listeParametreMCNP) == 4:
                return CSurfaceCollection(coneT4)
            if len(listeParametreMCNP) == 5:
                side = int(listeParametreMCNP[-1])
                plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                if typeSurfaceMCNP == MCNPS.K_X:
                    planeT4 = CSurfaceT4(T4S.PLANEX,
                                         [listeParametreMCNP[0]],
                                         idorigin=plane_idorigin)
                elif typeSurfaceMCNP == MCNPS.K_Y:
                    planeT4 = CSurfaceT4(T4S.PLANEY,
                                         [listeParametreMCNP[1]],
                                         idorigin=plane_idorigin)
                elif typeSurfaceMCNP == MCNPS.K_Z:
                    planeT4 = CSurfaceT4(T4S.PLANEZ,
                                         [listeParametreMCNP[2]],
                                         idorigin=plane_idorigin)
                return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])
            msg = ('Unexpected number of parameters in MCNP surface: {}'
                    .format(p_surfaceMCNP))
            raise ValueError(msg)
        elif typeSurfaceMCNP == MCNPS.X:
            # The meaning depends on lentgth of p and their relative position.
            if len(listeParametreMCNP) == 2:
                # only one pair is given. This is a px plane
                listeParametreT4 = [listeParametreMCNP[0]]
                typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PX]
                surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                  idorigin=idorigin)
                return CSurfaceCollection(surf)
            elif len(listeParametreMCNP) == 4:
                # Two points are given. This can be a px plane, a cx cylinder or a kx
                # cone.
                if listeParametreMCNP[0] == listeParametreMCNP[2]:
                    # this is a plane
                    listeParametreT4 = [listeParametreMCNP[0]]
                    typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PX]
                    surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                      idorigin=idorigin)
                    return CSurfaceCollection(surf)
                elif listeParametreMCNP[1] == listeParametreMCNP[3]:
                    # this is a cylinder
                    listeParametreT4 = [0, 0, listeParametreMCNP[1]]
                    typeSurfaceT4 = T4S.CYLX
                    surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                      idorigin=idorigin)
                    return CSurfaceCollection(surf)
                else:
                    # this is a cone
                    typeSurfaceT4 = T4S.CONEX
                    tana = (listeParametreMCNP[1] - listeParametreMCNP[3])\
                     / (listeParametreMCNP[0] - listeParametreMCNP[2])  # half-angle tan
                    x0 = listeParametreMCNP[0] - listeParametreMCNP[1]/tana
                    a = 180.*atan(tana)/pi
                    listeParametreT4 = [x0, 0, 0, fabs(a)]
                    coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                        idorigin=idorigin)
                    # we need a plane, too (one-nappe cone specified by MCNP
                    # manual §3.2.2.2)
                    side = 1 if listeParametreMCNP[0] > x0 else -1
                    plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                    planeT4 = CSurfaceT4(T4S.PLANEX, [x0],
                                         idorigin=plane_idorigin)
                    return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])
        elif typeSurfaceMCNP == MCNPS.Y:
            # The meaning depends on lentgth of p and their relative position.
            if len(listeParametreMCNP) == 2:
                # only one pair is given. This is a py plane
                listeParametreT4 = [listeParametreMCNP[0]]
                typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PY]
                surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                  idorigin=idorigin)
                return CSurfaceCollection(surf)
            elif len(listeParametreMCNP) == 4:
                # Two points are given. This can be a py plane, a cy cylinder or a ky
                # cone.
                if listeParametreMCNP[0] == listeParametreMCNP[2]:
                    # this is a plane
                    listeParametreT4 = [listeParametreMCNP[0]]
                    typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PY]
                    surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                      idorigin=idorigin)
                    return CSurfaceCollection(surf)
                elif listeParametreMCNP[1] == listeParametreMCNP[3]:
                    # this is a cylinder
                    listeParametreT4 = [0, 0, listeParametreMCNP[1]]
                    typeSurfaceT4 = T4S.CYLY
                    surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                      idorigin=idorigin)
                    return CSurfaceCollection(surf)
                else:
                    # this is a cone
                    typeSurfaceT4 = T4S.CONEY
                    tana = (listeParametreMCNP[1] - listeParametreMCNP[3])\
                     / (listeParametreMCNP[0] - listeParametreMCNP[2])  # half-angle tan
                    y0 = listeParametreMCNP[0] - listeParametreMCNP[1]/tana
                    a = 180.*atan(tana)/pi
                    listeParametreT4 = [0, y0, 0, fabs(a)]
                    coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                        idorigin=idorigin)
                    # we need a plane, too (one-nappe cone specified by MCNP
                    # manual §3.2.2.2)
                    side = 1 if listeParametreMCNP[0] > y0 else -1
                    plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                    planeT4 = CSurfaceT4(T4S.PLANEY, [y0],
                                         idorigin=plane_idorigin)
                    return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])
        elif typeSurfaceMCNP == MCNPS.Z:
            if len(listeParametreMCNP) == 2:
                listeParametreT4 = [listeParametreMCNP[0]]
                typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PZ]
                surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                  idorigin=idorigin)
                return CSurfaceCollection(surf)
            elif len(listeParametreMCNP) == 4:
                # Two points are given. This can be a px plane, a cx cylinder or a kx
                # cone.
                if listeParametreMCNP[0] == listeParametreMCNP[2]:
                    # this is a plane
                    listeParametreT4 = [listeParametreMCNP[0]]
                    typeSurfaceT4 = dict_conversionSurfaceType[MCNPS.PZ]
                    surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                      idorigin=idorigin)
                    return CSurfaceCollection(surf)
                elif listeParametreMCNP[1] == listeParametreMCNP[3]:
                    # this is a cylinder
                    listeParametreT4 = [0, 0, listeParametreMCNP[1]]
                    typeSurfaceT4 = T4S.CYLZ
                    surf = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                      idorigin=idorigin)
                    return CSurfaceCollection(surf)
                else:
                    # this is a cone
                    typeSurfaceT4 = T4S.CONEZ
                    tana = (listeParametreMCNP[1] - \
                    listeParametreMCNP[3]) / (listeParametreMCNP[0] - listeParametreMCNP[2])  # half-angle tan
                    a = 180.*atan(tana)/pi
                    z0 = listeParametreMCNP[0] - listeParametreMCNP[1]/tana
                    listeParametreT4 = [0, 0, z0, fabs(a)]
                    coneT4 = CSurfaceT4(typeSurfaceT4, listeParametreT4,
                                        idorigin=idorigin)
                    # we need a plane, too (one-nappe cone specified by MCNP
                    # manual §3.2.2.2)
                    side = 1 if listeParametreMCNP[0] > z0 else -1
                    plane_idorigin = idorigin + ['aux plane for nappe {}'.format(side)]
                    planeT4 = CSurfaceT4(T4S.PLANEZ, [z0],
                                         idorigin=plane_idorigin)
                    return CSurfaceCollection(coneT4, fixed=[(planeT4, side)])

        # Not a cone, fall back to the normal treatment
        if typeSurfaceMCNP in (MCNPS.TX, MCNPS.TY, MCNPS.TZ):
            listeParametreT4 = listeParametreMCNP
        elif (typeSurfaceMCNP in (MCNPS.PX, MCNPS.PY, MCNPS.PZ)
            and len(listeParametreMCNP) == 1):
            listeParametreT4 = listeParametreMCNP
        elif typeSurfaceMCNP == MCNPS.P and len(listeParametreMCNP) == 4:
            listeParametreT4 = [listeParametreMCNP[0], listeParametreMCNP[1],
                                listeParametreMCNP[2], -listeParametreMCNP[3]]
        elif typeSurfaceMCNP == MCNPS.S and len(listeParametreMCNP) == 4:
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

        surf = CSurfaceT4(typeSurfaceT4, listeParametreT4, idorigin=idorigin)
        return CSurfaceCollection(surf)

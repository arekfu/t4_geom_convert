# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''

from collections import OrderedDict
from MIP.geom.forcad import mcnp2cad
from MIP.geom.surfaces import get_surfaces
from MIP.geom.transforms import get_transforms
from ...Surface.CSurfaceMCNP import CSurfaceMCNP
from ...Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP
from ...Surface.ESurfaceTypeMCNP import string_to_enum, mcnp_to_mip
from ...Transformation.Transformation import transformation
from ...VectUtils import planeParamsFromPoints


def parseMCNPSurface(mcnpParser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the surfaces as a key
    and as a value, a object from the class CSurfaceMCNP
    '''
    surfaceParsed = get_surfaces(mcnpParser, lim=None)
    transformParsed = get_transforms(mcnpParser, lim=None)
    dictSurface = OrderedDict()
    n_surf = len(surfaceParsed)
    fmt_string = '\rparsing MCNP surface {{:{}d}}/{}'.format(len(str(n_surf)),
                                                             n_surf)
    for i, (k, v) in enumerate(surfaceParsed.items()):
        print(fmt_string.format(i+1), end='', flush=True)
        p_boundCond, p_transformation, p_typeSurface, l_paramSurface = v
        enumSurface = string_to_enum(p_typeSurface)
        enumSurface, l_paramSurface = normalizeSurface(enumSurface,
                                                       l_paramSurface)
        t, l_paramSurface, l_complParam, _ = mcnp2cad[mcnp_to_mip(enumSurface)](l_paramSurface)
        enumSurface = string_to_enum(t)
        idorigin = [k]
        if p_transformation:
            idorigin.append('via transformation {}'
                            .format(int(p_transformation)))
            surf = transformation(transformParsed[int(p_transformation)],
                                  enumSurface, l_paramSurface, l_complParam,
                                  p_boundCond, idorigin)
        else:
            surf = CSurfaceMCNP(p_boundCond, enumSurface, l_paramSurface,
                                l_complParam, idorigin)
        dictSurface[k] = surf
    print('... done', flush=True)

    return dictSurface


def normalizeSurface(typ, params):
    '''Put the surface parametrization in a canonical form. For instance,
    planes defined by three points are transformed into the equivalent
    (A,B,C,D) representation.'''
    if typ == ESurfaceTypeMCNP.P:
        if len(params) == 9:
            params = planeParamsFromPoints(params[0:3],
                                        params[3:6],
                                        params[6:9])
        elif len(params) != 4:
            raise ValueError('Planes "P" expect either 4 or 9 parameters')

    return typ, params

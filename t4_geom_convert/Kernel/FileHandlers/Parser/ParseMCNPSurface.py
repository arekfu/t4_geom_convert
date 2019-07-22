# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from MIP.geom.surfaces import get_surfaces
from ...Surface.CSurfaceMCNP import CSurfaceMCNP
from ...Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP
from ...Surface.ESurfaceTypeMCNP import string_to_enum
from collections import OrderedDict


def parseMCNPSurface(mcnpParser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the surfaces as a key
    and as a value, a object from the class CSurfaceMCNP
    '''
    surfaceParser = get_surfaces(mcnpParser, lim=None)
    dictSurface = OrderedDict()
    n_surf = len(surfaceParser)
    fmt_string = '\rparsing MCNP surface {{:{}d}}/{}'.format(len(str(n_surf)),
                                                             n_surf)
    for i, (k, v) in enumerate(surfaceParser.items()):
        print(fmt_string.format(i+1), end='', flush=True)
        p_boundCond, p_transformation, p_typeSurface, l_paramSurface = v
        if p_transformation:
            continue
        enumSurface = string_to_enum(p_typeSurface)
        dictSurface[k] = CSurfaceMCNP(p_boundCond, p_transformation,
                                        enumSurface, l_paramSurface)
    print('... done', flush=True)

    return dictSurface

# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
'''

from collections import OrderedDict

from MIP.geom.surfaces import get_surfaces
from MIP.geom.transforms import get_transforms

from .Transformation import transformation
from .CSurfaceTransformed import CSurfaceTransformed
from ..Surface.ESurfaceTypeMCNP import string_to_enum


def surfaceTransformed(mcnpParser):
    transformParsed = get_transforms(mcnpParser, lim=None)
    surfaceParser = get_surfaces(mcnpParser, lim=None)
    dictSurfaceTransformed = OrderedDict()
    for k, v in list(surfaceParser.items()):
        p_boundCond, p_transformation, p_typeSurface, l_paramSurface = v
        idorigin = [k]
        if p_transformation:
            enumSurface = string_to_enum(p_typeSurface)
            idorigin.append('via transformation {}'.format(p_transformation))
            dictSurfaceTransformed[k] = transformation(p_boundCond,
                                                       transformParsed[int(p_transformation)],
                                                       enumSurface,
                                                       l_paramSurface,
                                                       idorigin)
    return dictSurfaceTransformed

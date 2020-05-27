# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from .ConversionSurfaceMCNPToT4 import convert_mcnp_surfaces
from ..FileHandlers.Parser.ParseMCNPSurface import parseMCNPSurface


def construct_surface_t4(mcnp_parser):
    '''
    :brief: method constructing a dictionary with the id
    of the surface as a key and the instance of SurfaceT4 as a value
    '''
    dic_surface_mcnp = parseMCNPSurface(mcnp_parser)
    dic_surface_t4 = convert_mcnp_surfaces(dic_surface_mcnp)

    return dic_surface_t4, dic_surface_mcnp

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


def parseMCNPSurface(mcnp_parser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the surfaces as a key
    and as a value, a object from the class CSurfaceMCNP
    '''
    surface_parsed = get_surfaces(mcnp_parser, lim=None)
    transform_parsed = get_transforms(mcnp_parser, lim=None)
    dict_surface = OrderedDict()
    n_surf = len(surface_parsed)
    fmt_string = '\rparsing MCNP surface {{:{}d}}/{}'.format(len(str(n_surf)),
                                                             n_surf)
    for i, (key, surface) in enumerate(surface_parsed.items()):
        print(fmt_string.format(i+1), end='', flush=True)
        dict_surface[key] = to_surface_mcnp(key, surface, transform_parsed)
    print('... done', flush=True)

    return dict_surface


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


def to_surface_mcnp(key, parsed_surface, transform_parsed):
    '''Convert the surface described by the given type parameters to a
    :class:`CSurfaceMCNP`.'''
    bound_cond, transform_id, type_surface, params = parsed_surface
    enum_surface = string_to_enum(type_surface)
    enum_surface, params = normalizeSurface(enum_surface, params)
    mip_transf = mcnp2cad[mcnp_to_mip(enum_surface)]
    typ, params, compl_params, _ = mip_transf(params)
    enum_surface = string_to_enum(typ)
    idorigin = [key]
    if transform_id:
        idorigin.append('via transformation {}'
                        .format(int(transform_id)))
        surf = transformation(transform_parsed[int(transform_id)],
                              enum_surface, params, compl_params,
                              bound_cond, idorigin)
    else:
        surf = CSurfaceMCNP(bound_cond, enum_surface, params,
                            compl_params, idorigin)
    return surf

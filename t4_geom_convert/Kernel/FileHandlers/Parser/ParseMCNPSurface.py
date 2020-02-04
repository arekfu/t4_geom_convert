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
from ...Surface.SurfaceMCNP import SurfaceMCNP
from ...Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS
from ...Surface.ESurfaceTypeMCNP import string_to_enum, mcnp_to_mip
from ...Transformation.Transformation import transformation
from ...VectUtils import planeParamsFromPoints
from ...Surface import MacroBodies as MB


def parseMCNPSurface(mcnp_parser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the surfaces as a key
    and as a value, a object from the :class:`SurfaceMCNP` class.
    '''
    surface_parsed = get_surfaces(mcnp_parser, lim=None)
    transform_parsed = get_transforms(mcnp_parser, lim=None)
    dict_surface = OrderedDict()
    n_surf = len(surface_parsed)
    fmt_string = ('\rparsing MCNP surface {{:{}d}} ({{:3d}}%)'
                  .format(len(str(max(surface_parsed)))))
    for i, (key, surface) in enumerate(surface_parsed.items()):
        percent = int(100.0*i/(n_surf-1)) if n_surf > 1 else 100
        print(fmt_string.format(key, percent), end='', flush=True)
        dict_surface[key] = to_surfaces_mcnp(key, surface, transform_parsed)
    print('... done', flush=True)

    return dict_surface


def normalizeSurface(typ, params):
    '''Put the surface parametrization in a canonical form. For instance,
    planes defined by three points are transformed into the equivalent
    (A,B,C,D) representation.'''
    if typ == MS.P:
        if len(params) == 9:
            params = planeParamsFromPoints(params[0:3],
                                           params[3:6],
                                           params[6:9])
        elif len(params) != 4:
            raise ValueError('Planes "P" expect either 4 or 9 parameters')

    return typ, params


def to_surface_mcnp(key, bound_cond,  # pylint: disable=too-many-arguments
                    transform_id, enum_surface, params, transform_parsed):
    '''Convert the parsed surface into a :class:`SurfaceMCNP`.'''
    enum_surface, params = normalizeSurface(enum_surface, params)
    mip_transf = mcnp2cad[mcnp_to_mip(enum_surface)]
    typ, params, compl_params, _ = mip_transf(params)
    enum_surface = string_to_enum(typ)
    idorigin = [key]
    surf = SurfaceMCNP(bound_cond, enum_surface, params,
                       compl_params, idorigin)
    if transform_id:
        idorigin.append('via transformation {}'
                        .format(int(transform_id)))
        surf = transformation(transform_parsed[int(transform_id)], surf)
    return surf


def to_surfaces_macro(key, bound_cond,  # pylint: disable=too-many-arguments
                      transform_id, enum_surface, params, transform_parsed):
    '''Convert the parsed macro body into a collection of
    :class:`SurfaceMCNP`.'''
    if enum_surface == MS.BOX:
        parts = MB.box(params)
    elif enum_surface == MS.RPP:
        parts = MB.rpp(params)
    elif enum_surface == MS.SPH:
        parts = MB.sph(params)
    elif enum_surface == MS.RCC:
        parts = MB.rcc(params)
    elif enum_surface in (MS.RHP, MS.HEX):
        parts = MB.rhp(params)
    elif enum_surface == MS.REC:
        parts = MB.rec(params)
    elif enum_surface == MS.TRC:
        parts = MB.trc(params)
    elif enum_surface == MS.ELL:
        parts = MB.ell(params)
    elif enum_surface == MS.WED:
        parts = MB.wed(params)
    elif enum_surface == MS.ARB:
        parts = MB.arb(params)
    else:
        raise NotImplementedError('Macrobody {} is not implemented yet'
                                  .format(enum_surface))
    mcnp_surfs = [(to_surface_mcnp(key, bound_cond, transform_id, type_,
                                   params, transform_parsed), side)
                  for type_, params, side in parts]
    return mcnp_surfs


def to_surfaces_mcnp(key, parsed_surface, transform_parsed):
    '''Convert the parsed surface into a collection of
    :class:`SurfaceMCNP`.

    This function returns a list of ``(int, SurfaceMCNP)`` pairs. The integers
    represent the side of the surface that should be considered as positive
    (±1).'''
    bound_cond, transform_id, type_surface, params = parsed_surface
    enum_surface = string_to_enum(type_surface)
    if enum_surface in (MS.BOX, MS.RPP, MS.SPH, MS.RCC, MS.HEX, MS.RHP, MS.REC,
                        MS.TRC, MS.ELL, MS.WED, MS.ARB):
        return to_surfaces_macro(key, bound_cond, transform_id, enum_surface,
                                 params, transform_parsed)
    surf = to_surface_mcnp(key, bound_cond, transform_id, enum_surface, params,
                           transform_parsed)
    return [(surf, 1)]

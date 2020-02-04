# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
'''

from MIP.geom.forcad import transform_frame

from ..Surface.SurfaceMCNP import SurfaceMCNP
from .TransformationQuad import transformation_quad
from .TransformationError import TransformationError

from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS


def transformation(trpl, surface):
    '''Apply a transformation to the given surface parameters.

    :param trpl: the transformation
    :param type_surf: the surface type
    :param frame: the surface frame
    :param params: the surface parameters, if any
    :param bound: the boundary conditions attached to the surface
    :param idorigin: a list of origin information about this surface
    '''
    if not trpl:
        return surface
    if surface.type_surface == MS.GQ:
        frame = tuple(surface.param_surface)
        params = transformation_quad(surface.compl_param, trpl)
    else:
        frame = transform_frame(surface.param_surface, trpl)
        params = list(surface.compl_param)
        if surface.type_surface in (MS.K, MS.K_X, MS.K_Y, MS.K_Z, MS.KX, MS.KY,
                                    MS.KZ):
            if len(params) == 2 or len(params) == 4:
                params.append(None)
            elif len(params) == 3 or len(params) == 5:
                params.append(params[-1])
            else:
                msg = ('Unexpected number of parameters for cone: {}'
                       .format(params))
                raise TransformationError(msg)
    return SurfaceMCNP(surface.boundary_cond, surface.type_surface, frame,
                       params, surface.idorigin)

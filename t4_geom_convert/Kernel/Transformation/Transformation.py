# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
'''

from MIP.geom.forcad import transform_frame

from ..Surface.CSurfaceMCNP import CSurfaceMCNP
from .TransformationQuad import transformationQuad

from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS


def transformation(trpl, type_surf, frame, params, bound, idorigin):
    '''Apply a transformation to the given surface parameters.

    :param trpl: the transformation
    :param type_surf: the surface type
    :param frame: the surface frame
    :param params: the surface parameters, if any
    :param bound: the boundary conditions attached to the surface
    :param idorigin: a list of origin information about this surface
    '''
    if not trpl:
        return CSurfaceMCNP(bound, type_surf, frame, params, idorigin)
    if type_surf == MS.GQ:
        params = transformationQuad(params, trpl)
    else:
        frame = transform_frame(frame, trpl)
        if type_surf in (MS.K, MS.K_X, MS.K_Y, MS.K_Z, MS.KX, MS.KY, MS.KZ):
            params = list(params)
            if len(params) == 2 or len(params) == 4:
                params.append(None)
            elif len(params) == 3 or len(params) == 5:
                params.append(params[-1])
            else:
                raise ValueError('Unexpected number of parameters for cone: {}'
                                 .format(params))
    return CSurfaceMCNP(bound, type_surf, frame, params, idorigin)

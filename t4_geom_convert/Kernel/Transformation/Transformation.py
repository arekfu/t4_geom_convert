# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
'''

from collections import OrderedDict

from MIP.geom.forcad import transform_frame
from MIP.geom.transforms import get_transforms

from ..Surface.SurfaceMCNP import SurfaceMCNP
from .TransformationQuad import transformation_quad
from .TransformationError import TransformationError

from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS



def get_mcnp_transforms(parser):
    '''Return the dictionary of parsed MCNP transformation, in a canonical,
    12-parameter form.

    :param parser: the MCNP parser
    :returns: a dictionary associating each transformation number to a list of
        12 transformation parameters.
    '''
    mcnp_transforms = get_transforms(parser)
    transforms = OrderedDict()
    for transf_id, transf in mcnp_transforms.items():
        if len(transf) == 12 or transf[-1] == 1:
            transforms[transf_id] = transf[:12]
        else:
            raise ValueError('Transformations with m=-1 are not supported '
                             'yet. The problematic transformation was TR{}={}'
                             .format(transf_id, transf))
    return transforms


def transformation(trpl, surface):
    '''Apply a transformation to the given surface parameters.

    :param trpl: the transformation
    :param SurfaceMCNP surface: an MCNP surface
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

# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CSurfaceMCNP.py
'''

from ..VectUtils import planeParamsFromPoints
from .ESurfaceTypeMCNP import ESurfaceTypeMCNP

class CSurfaceMCNP:
    '''
    :brief: Class which permit to access precisely to the information of the block SURFACE of MCNP
    '''

    def __init__(self, p_boundaryCond, p_typeSurface, l_paramSurface,
                 l_complParam, l_idorigin=None):
        '''
        Constructor
        :param: p_boundaryCond : parameter 1 of the boundary condition
        :param: p_typeSurface : string specifying the type of the Surface
        :param: l_paramSurface : list of parameter describing the surface
        :param: l_complParam : list of parameter describing the surface
        '''
        self.boundaryCond = p_boundaryCond
        self.typeSurface = p_typeSurface
        self.paramSurface = l_paramSurface
        self.complParam = l_complParam
        self.idorigin = l_idorigin.copy() if l_idorigin is not None else []

    def __repr__(self):
        return ('CSurfaceMCNP({!r}, {!r}, {!r}, {!r}, {!r})'
                .format(self.boundaryCond, self.typeSurface, self.paramSurface,
                        self.complParam, self.idorigin))

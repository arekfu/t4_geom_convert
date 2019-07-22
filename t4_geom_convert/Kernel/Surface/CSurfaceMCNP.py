# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CSurfaceMCNP.py
'''

class CSurfaceMCNP:
    '''
    :brief: Class which permit to access precisely to the information of the block SURFACE of MCNP
    '''


    def __init__(self, p_boundaryCond, p_transformation, p_typeSurface, l_paramSurface, l_idorigin=None):
        '''
        Constructor
        :param: p_boundaryCond : parameter 1 of the boundary condition
        :param: p_transformation : transformation apply on the Surface
        :param: p_typeSurface : string specifying the type of the Surface
        :param: l_paramSurface : list of parameter describing the surface
        '''
        self.boundaryCond = p_boundaryCond
        self.transformation = p_transformation
        self.typeSurface = p_typeSurface
        self.paramSurface = l_paramSurface
        self.idorigin = l_idorigin.copy() if l_idorigin is not None else []

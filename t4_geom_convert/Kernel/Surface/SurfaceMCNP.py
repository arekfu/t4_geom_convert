# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : SurfaceMCNP.py
'''


class SurfaceMCNP:
    '''Class that contains the information of the MCNP surface cards.'''

    def __init__(self, boundary_cond, type_surface, param_surface,
                 compl_param, idorigin=None):
        '''
        Constructor
        :param boundary_cond: parameter 1 of the boundary condition
        :param type_surface: string specifying the type of the Surface
        :param param_surface: list of parameter describing the surface
        :param compl_param: list of parameter describing the surface
        :param idorigin: a list of things that describe where this surface
            comes from
        '''
        self.boundary_cond = boundary_cond
        self.type_surface = type_surface
        self.param_surface = tuple(param_surface)
        self.compl_param = tuple(compl_param)
        self.idorigin = tuple(idorigin) if idorigin is not None else ()

    def __repr__(self):
        return ('SurfaceMCNP({!r}, {!r}, {!r}, {!r}, {!r})'
                .format(self.boundary_cond, self.type_surface,
                        self.param_surface, self.compl_param, self.idorigin))

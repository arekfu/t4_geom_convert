# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CSurfaceMCNP.py
'''

class CSurfaceT4:
    '''
    :brief: Class which permit to access precisely to the information of the block SURFACE of T4
    '''

    def __init__(self, p_typeSurface, l_paramSurface, idorigin=None):
        '''
        Constructor
        :param: p_typeSurface : string specifying the type of the Surface
        :param: l_paramSurface : list of parameter describing the surface
        '''

        self.typeSurface = p_typeSurface
        self.paramSurface = l_paramSurface
        self.idorigin = idorigin.copy() if idorigin is not None else []

    def __repr__(self):
        return 'CSurfaceT4({!r}, {!r}, {!r})'.format(self.typeSurface,
                                                     self.paramSurface,
                                                     self.idorigin)

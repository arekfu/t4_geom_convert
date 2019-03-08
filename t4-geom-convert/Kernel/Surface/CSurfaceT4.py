# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CSurfaceMCNP.py
'''

class CSurfaceT4(object):
    '''
    :brief: Class which permit to access precisely to the information of the block SURFACE of T4
    '''


    def __init__(self, p_typeSurface, l_paramSurface):
        '''
        Constructor
        :param: p_un : parameter 1 of the tuple Surface
        :param: p_deux : parameter 2 of the tuple Surface
        :param: p_typeSurface : string specifying the type of the Surface
        :param: l_paramSurface : list of parameter describing the surface
        '''

        self.typeSurface = p_typeSurface
        self.paramSurface = l_paramSurface
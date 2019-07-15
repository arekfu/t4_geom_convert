# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CParseMCNPSurface.py

.. doctest:: CParseMCNPSurface
    :hide:
    >>> from CParseMCNPSurface import CParseMCNPSurface
    >>> objet_MCNPSurface = CParseMCNPSurface()
    >>> dict_Surface = objet_MCNPSurface.m_parsingSurface()
    >>> print(dict_Surface)

'''
from MIP import mip
from MIP.geom.surfaces import get_surfaces
from ...Surface.CSurfaceMCNP import CSurfaceMCNP
from ...Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP
from ...Configuration.CConfigParameters import CConfigParameters
from ...Surface.ESurfaceTypeMCNP import string_to_enum
from collections import OrderedDict

class CParseMCNPSurface(object):
    '''
    :brief: Class which parse the block Surface
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().m_readNameMCNPInputFile()

    def m_parsingSurface(self):
        '''
        :brief method which permit to recover the information of each line
        of the block SURFACE
        :return: dictionary which contains the ID of the surfaces as a key
        and as a value, a object from the class CSurfaceMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        surfaceParser = get_surfaces(inputCell, lim=None)
        dictSurface = OrderedDict()
        for k, v in list(surfaceParser.items()):
            p_boundCond, p_transformation, p_typeSurface, l_paramSurface = v
            if p_transformation:
                continue
            enumSurface = string_to_enum(p_typeSurface)
            dictSurface[k] = CSurfaceMCNP(p_boundCond, p_transformation,\
                                           enumSurface, l_paramSurface)
        return dictSurface

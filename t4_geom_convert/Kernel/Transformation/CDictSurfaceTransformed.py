# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
:file : CDictSurfaceTransformed.py

.. doctest:: CParseMCNPSurface
    :hide:
    >>> from CParseMCNPSurface import CParseMCNPSurface
    >>> objet_MCNPSurface = CParseMCNPSurface()
    >>> dict_Surface = objet_MCNPSurface.parsingSurface()
    >>> print(dict_Surface)

'''

from collections import OrderedDict

from MIP import mip
from MIP.geom.surfaces import get_surfaces
from MIP.geom.transforms import get_transforms

from .CTransformationFonction import CTransformationFonction
from .CSurfaceTransformed import CSurfaceTransformed
from ..Configuration.CConfigParameters import CConfigParameters
from ..Surface.ESurfaceTypeMCNP import string_to_enum

class CDictSurfaceTransformed(object):
    '''
    :brief: Class which parse the block Surface
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().readNameMCNPInputFile()

    def surfaceTransformed(self):
        inputCell = mip.MIP(self.inputMCNP)
        transformParsed = get_transforms(inputCell, lim=None)
        surfaceParser = get_surfaces(inputCell, lim=None)
        dictSurfaceTransformed = OrderedDict()
        for k, v in list(surfaceParser.items()):
            p_boundCond, p_transformation, p_typeSurface, l_paramSurface = v
            idorigin = [k]
            if p_transformation:
                enumSurface = string_to_enum(p_typeSurface)
                idorigin.append('via transformation {}'.format(p_transformation))
                dictSurfaceTransformed[k] = CTransformationFonction().transformation(p_boundCond, transformParsed[int(p_transformation)], enumSurface, l_paramSurface, idorigin)
        return dictSurfaceTransformed

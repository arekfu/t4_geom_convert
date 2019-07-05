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
    >>> dict_Surface = objet_MCNPSurface.m_parsingSurface()
    >>> print(dict_Surface)

'''

from ..Configuration.CConfigParameters import CConfigParameters
from ..Transformation.CTransformationFonction import CTransformationFonction
from ...MIP import mip
from ...MIP.geom.surfaces import get_surfaces
from ..Transformation.CSurfaceTransformed import CSurfaceTransformed
from ..Surface.ESurfaceTypeMCNP import string_to_enum
from ...MIP.geom.transforms import get_transforms
from collections import OrderedDict

class CDictSurfaceTransformed(object):
    '''
    :brief: Class which parse the block Surface
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().m_readNameMCNPInputFile()
    
    def m_surfaceTransformed(self):
        inputCell = mip.MIP(self.inputMCNP)
        transformParsed = get_transforms(inputCell, lim=None)
#         print(transformParsed)
        surfaceParser = get_surfaces(inputCell, lim=None)
        dictSurfaceTransformed = OrderedDict()
        for k, v in list(surfaceParser.items()):
            p_boundCond, p_transformation, p_typeSurface, l_paramSurface = v
#             print(p_typeSurface)
            if p_transformation:
                enumSurface = string_to_enum(p_typeSurface)
                dictSurfaceTransformed[k] = CTransformationFonction().m_transformation(p_boundCond, transformParsed[int(p_transformation)], enumSurface, l_paramSurface)
        return dictSurfaceTransformed


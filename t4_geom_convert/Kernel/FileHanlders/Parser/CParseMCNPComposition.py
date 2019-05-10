# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
:file : CParseMCNPComposition.py

.. doctest:: CParseMCNPComposition
    :hide:
    >>> from CParseMCNPComposition import CParseMCNPComposition
    >>> objet_MCNPComposition = CParseMCNPComposition()
    >>> dict_Composition = objet_MCNPCell.m_parsingMaterialComposition()
    >>> print(dict_Composition)

'''
from ....MIP import mip
from ...Composition.CCompositionMCNP import CCompositionMCNP
from ....MIP.geom.grammars.composition import get_materialComposition
from ...Configuration.CConfigParameters import CConfigParameters

class CParseMCNPComposition(object):
    '''
    :brief: Class which parse the material part of the block data
    '''


    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().m_readNameMCNPInputFile()

    def m_parsingMaterialComposition(self):
        '''
        :brief method which permit to recover the information of each line
        of the block SURFACE
        :return: dictionary which contains the ID of the materials as a key
        and as a value, a object from the class CCompositionMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        compositionParser = get_materialComposition(inputCell, lim=None)
        dictComposition = dict()
        for k, v in list(compositionParser.items()):
            l_materialCompositionParameters = v
            dictComposition[k] = CCompositionMCNP(l_materialCompositionParameters)
        return dictComposition

# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
:file : CParseMCNPComposition.py
'''
from geom.composition import get_materialComposition
import mip

from FileHanlders.Parser.Parameters import f_inputMCNP
from Composition.CCompositionMCNP import CCompositionMCNP

class CParseMCNPComposition(object):
    '''
    :brief: Class which parse the material part of the block data
    '''


    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = f_inputMCNP
        
    def m_parsingMaterialComposition(self):
        
        '''
        :brief method which permit to recover the information of each line of the block SURFACE
        :return: dictionary which contains the ID of the materials as a key and as a value, a object from the class CCompositionMCNP
        '''
        
        inputCell = mip.MIP(self.inputMCNP)
        compositionParser = get_materialComposition(inputCell, lim=None)
        dictComposition = dict()
        for k,v in list(compositionParser.items()):
            l_materialCompositionParameters = v
            dictComposition[k] = CCompositionMCNP(l_materialCompositionParameters)
        return dictComposition
        


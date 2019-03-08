# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CParseMCNPTransform.py
'''
import mip
from geom.transforms import get_transforms
from FileHanlders.Parser.Parameters import f_inputMCNP
from Surface.CTransformationMCNP import CTransformationMCNP

class CParseMCNPTransform(object):
    '''
    :brief: Class which parse the transformation part of the block data
    '''


    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = f_inputMCNP
        
    def m_parsingTransform(self):
        
        '''
        :brief method which permit to recover the information of each line of the transform part of the block DATA
        :return: dictionary which contains the ID of the transformations as a key and as a value, a object from the class CTransformMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        transformParser = get_transforms(inputCell, lim=None)
        dictSurface = dict()
        for k,v in list(transformParser.items()):
            l_transformationParameters = v
            l_originTransformation = l_transformationParameters[0:3]
            l_rotationTransformation = l_transformationParameters[3:12]
            dictSurface[k] = CTransformationMCNP(l_originTransformation, l_rotationTransformation)
        return dictSurface
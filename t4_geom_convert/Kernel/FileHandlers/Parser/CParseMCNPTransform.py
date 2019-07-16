# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CParseMCNPTransform.py

.. doctest:: CParseMCNPTransform
    :hide:
    >>> from CParseMCNPTransform import CParseMCNPTransform
    >>> objet_MCNPTransform = CParseMCNPTransform()
    >>> dict_Transform = objet_MCNPTransform.parsingTransform()
    >>> print(dict_Transform)

'''
from MIP import mip
from MIP.geom.transforms import get_transforms
from ...Surface.CTransformationMCNP import CTransformationMCNP
from ...Configuration.CConfigParameters import CConfigParameters
from collections import OrderedDict

class CParseMCNPTransform(object):
    '''
    :brief: Class which parse the transformation part of the block data
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().readNameMCNPInputFile()

    def parsingTransform(self):
        '''
        :brief method which permit to recover the information of each line
        of the transform part of the block DATA
        :return: dictionary which contains the ID of the transformations
        as a key and as a value, a object from the class CTransformMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        transformParser = get_transforms(inputCell, lim=None)
        dictSurface = OrderedDict()
        for k, v in list(transformParser.items()):
            l_transformationParameters = v
            l_originTransformation = l_transformationParameters[0:3]
            l_rotationTransformation = l_transformationParameters[3:12]
            dictSurface[k] = CTransformationMCNP(l_originTransformation,
                                                 l_rotationTransformation)
        return dictSurface

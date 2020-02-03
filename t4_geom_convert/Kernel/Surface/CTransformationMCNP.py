# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CTransformMCNP.py
'''

class CTransformationMCNP:
    '''
     :brief: Class which permit to access precisely to the information of
     the transformation part of the block DATA
    '''

    def __init__(self, l_originTransformation, l_rotationTransformation):
        '''
        Constructor
        :param: l_originTransformation : list of the coordinates points of
        the new cartesian axes
        :param: l_rotationTransformation : coordinates of the matrix of rotation
        '''
        self.originTransformation = l_originTransformation
        self.rotationTransformation = l_rotationTransformation

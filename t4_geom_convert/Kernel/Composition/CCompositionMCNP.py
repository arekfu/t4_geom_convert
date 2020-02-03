# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
:file : CCompositionMCNP.py
'''
import math
class CCompositionMCNP:
    '''
    :brief: Class which permit to access precisely to the information
    of the part material of the block DATA
    '''

    def __init__(self, l_materialCompositionParameters):
        '''
        Constructor
        :param: l_materialCompositionParameters : list of composition of
        material with id of isotope and its abondance
        '''
        self.materialCompositionParameters = []
        i = 0
        while i < len(l_materialCompositionParameters):
            isotope = l_materialCompositionParameters[i]
            if '=' in isotope:
                # this is a keyword, skip it
                i += 1
                continue
            if "." in isotope:
                isotope = isotope.split(".")[0]
            fractionIsotope = l_materialCompositionParameters[i+1]
            self.materialCompositionParameters.append((isotope,
                                                       fractionIsotope))
            i += 2

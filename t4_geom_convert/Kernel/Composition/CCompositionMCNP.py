# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
:file : CCompositionMCNP.py
'''
import math
class CCompositionMCNP(object):
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
        self.materialCompositionParameters = l_materialCompositionParameters

    def ordDict(self):
        '''
        :brief: method taking the liste of the parameters of the composition
        in the MCNP file and return a list reordonate in list of tuple :
        isotope, fractionOfTheIsotope
        '''
        L = []
        for i in range(0, math.floor(len(self.materialCompositionParameters)/2.0)):
            isotope = self.materialCompositionParameters[2*i]
            if "." in isotope:
                l_isotope = isotope.split(".")
                isotope = l_isotope[0]
            fractionIsotope = self.materialCompositionParameters[(2*i)+1]
            L.append((isotope, fractionIsotope))
        self.materialCompositionParameters = L
        return self.materialCompositionParameters

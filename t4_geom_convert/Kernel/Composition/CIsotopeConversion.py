# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
:file : CIsotopeConversion.py
'''
from .EIsotopeAtomicNumberMCNP import EIsotopeAtomicNumber

class CIsotopeConversion(object):
    '''
    :brief: Class which structures the characteristics of the isotope
    '''


    def __init__(self, p_isotopeId):
        '''
        Constructor
        '''
        self.isotopeId = p_isotopeId

    def conversionIsotope(self):
        '''
        :brief: method which takes a string and returns a tuple of enum and string
        '''

        massNumber = str(int(self.isotopeId[-3:]))
        atomicNumber = self.isotopeId[0:-3]
        atomicNumber = getattr(EIsotopeAtomicNumber, atomicNumber)
        return atomicNumber, massNumber

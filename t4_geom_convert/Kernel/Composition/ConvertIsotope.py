# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
:file : ConvertIsotope.py
'''
from .EIsotopeAtomicNumberMCNP import EIsotopeAtomicNumber

def convert_isotope(isotope_id):
    '''
    :brief: method which takes a string and returns a tuple of enum and string
    '''

    isotope_id = isotope_id.split('.')[0]
    massNumber = str(int(isotope_id[-3:]))
    atomicNumber = getattr(EIsotopeAtomicNumber, isotope_id[0:-3])
    return atomicNumber, massNumber

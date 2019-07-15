# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
:file : CCompositionConversionMCNPToT4.py
'''

from ..Composition.CDictCompositionT4 import CDictCompositionT4
from ..Composition.CDictCompositionMCNP import CDictCompositionMCNP
from ..Composition.CIsotopeConversion import CIsotopeConversion
from ..Composition.EIsotopeNameElementT4 import EIsotopeNameElement
from collections import OrderedDict
from math import fabs

class CCompositionConversionMCNPToT4(object):
    '''
    :brief: Class transforming materials information from MCNP in composition T4
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def m_conversionCompositionMCNPToT4(self):
        '''
        :brief: method recuperate the dictionary of the composition from MCNP
        and return a dictionary of the composition for T4
        '''
        d_CompositionT4 = OrderedDict()
        obj_T4 = CDictCompositionT4(d_CompositionT4)
        l_compositionT4 = []
        for key, val in CDictCompositionMCNP().d_compositionMCNP.items():
            l_compositionT4 = []
            listMaterialsSurface = val.m_ordDict()
            for element in listMaterialsSurface:
                isotopeId, fraction = element
                atomicNumber, massNumber = CIsotopeConversion(isotopeId).m_conversionIsotope()
                atomicNumberT4 = EIsotopeNameElement(atomicNumber.value)
                if massNumber == '0':
                    massNumberT4 = '-NAT'
                else:
                    massNumberT4 = massNumber
                isotopeT4 = atomicNumberT4, massNumberT4
                l_compositionT4.append((isotopeT4, str(fabs(float(fraction)))))
            valueT4 = l_compositionT4
            obj_T4.__setitem__(key, valueT4)    
        return d_CompositionT4
# d = CCompositionConversionMCNPToT4().m_conversionCompositionMCNPToT4()
# for key,val in d.items():
#     print(key,val)

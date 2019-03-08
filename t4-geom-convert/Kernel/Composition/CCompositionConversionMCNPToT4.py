# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
:file : CCompositionConversionMCNPToT4.py
'''
from Surface.CDictSurfaceMCNP import CDictSurfaceMCNP
from Surface.CDictSurfaceT4 import CDictSurfaceT4
from Surface.DTypeConversion import dict_conversionSurfaceType
import math
from Composition.CDictCompositionT4 import CDictCompositionT4
from Composition.CDictCompositionMCNP import CDictCompositionMCNP
from Composition.CIsotopeConversion import CIsotopeConversion
from Composition.EIsotopeNameElementT4 import EIsotopeNameElement

class CCompositionConversionMCNPToT4(object):
    '''
    :brief: Class transforming materials information from MCNP in composition T4
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    
    def m_conversionCompositionMCNPToT4(self):
        
        dic_CompositionT4 = dict()
        obj_T4 = CDictCompositionT4(dic_CompositionT4)
        l_compositionT4 = []
        for key,val in CDictCompositionMCNP().d_compositionMCNP.items() :
            listMaterialsSurface = val.m_ordDict()
            for element in listMaterialsSurface:
                isotopeId, fraction = element
                atomicNumber, massNumber = CIsotopeConversion(isotopeId).m_conversionIsotope()
                atomicNumberT4 = EIsotopeNameElement(atomicNumber.value)
                if massNumber == '000':
                    massNumberT4 = '-NAT'
                else:
                    massNumberT4 = massNumber
                #print(massNumberT4)
                isotopeT4 = atomicNumberT4, massNumberT4
                l_compositionT4.append((isotopeT4, fraction))
            valueT4 = l_compositionT4
            obj_T4.__setitem__(key, valueT4)
            
        return dic_CompositionT4
    
# d = CCompositionConversionMCNPToT4().m_conversionCompositionMCNPToT4()
# for key,val in d.items():
#     print(key,val)
    


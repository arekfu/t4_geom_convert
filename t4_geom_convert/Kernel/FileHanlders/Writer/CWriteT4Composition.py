# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4Composition..py
'''
from ...Composition.CIntermediateCompositionT4 import CIntermediateCompositionT4

class CWriteT4Composition(object):
    '''
    :brief: Class which write the geometry part of the T4 input file
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def m_writeT4Composition(self):
        '''
        :brief: method writing composition of the T4 input file
        '''
        f = open('testconnverti.txt',"a+")
        f.write("\r\n COMPOSITION \r\n")
        f.write("\r\n")
        temperature = 300
        dic_composition = CIntermediateCompositionT4().m_constructCompositionT4()
        for k in dic_composition.keys():
            s_paramMaterialComposition = ''
            p_typeDensity = dic_composition[k].typeDensity
            p_materialName = dic_composition[k].material
            p_densityValue = dic_composition[k].valueOfDensity
            p_numberOfIsotope = dic_composition[k].numberOfIsotope
            list_isotope = dic_composition[k].listMaterialComposition
            for element in list_isotope:
                nameIsotope, abondanceIsotope = element
                s_paramMaterialComposition = s_paramMaterialComposition +\
                str(nameIsotope) + ' ' + str(abondanceIsotope) +' '
                print(s_paramMaterialComposition)
            f.write("%s %s %s %s %s %s \r" % (p_typeDensity, temperature,\
                                              p_materialName,p_densityValue,\
                                              p_numberOfIsotope,\
                                              s_paramMaterialComposition))
        f.write("\r\n")
        f.write("END_COMPOSITION")
        f.close()

CWriteT4Composition().m_writeT4Composition()

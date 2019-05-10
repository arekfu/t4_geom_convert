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
    def m_writeT4Composition(self, f):
        '''
        :brief: method writing composition of the T4 input file
        '''
        f.write("\n COMPOSITION \n")
        f.write("\n")
        temperature = 300
        dic_composition = CIntermediateCompositionT4().m_constructCompositionT4()
        for k in dic_composition.keys():
            s_paramMaterialComposition = ''
            l_typeDensity = dic_composition[k].typeDensity
            l_densityValue = dic_composition[k].valueOfDensity
            p_numberOfIsotope = dic_composition[k].numberOfIsotope
            list_isotope = dic_composition[k].listMaterialComposition
            for element in list_isotope:
                nameIsotope, abondanceIsotope = element
                s_paramMaterialComposition = s_paramMaterialComposition +\
                str(nameIsotope) + ' ' + str(abondanceIsotope) +' '
            for i in range(0,len(l_densityValue)):
                p_materialName = dic_composition[k].material
                f.write("%s %s %s %s %s %s \n" % (l_typeDensity[i], temperature,\
                                              p_materialName,abs(l_densityValue[i]),\
                                              p_numberOfIsotope,\
                                              s_paramMaterialComposition))
                p_materialName += str(i*1000)
        f.write("\n")
        f.write("END_COMPOSITION")
        f.write("\n")

# CWriteT4Composition().m_writeT4Composition()

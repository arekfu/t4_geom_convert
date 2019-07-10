# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4Composition..py
'''
from ...Composition.CIntermediateCompositionT4 import CIntermediateCompositionT4
from math import fabs

class CWriteT4Composition(object):
    '''
    :brief: Class which write the geometry part of the T4 input file
    '''

    def __init__(self, mcnp_new_dict):
        '''
        Constructor
        '''
        self.mcnp_new_dict = mcnp_new_dict
    def m_writeT4Composition(self, f):
        '''
        :brief: method writing composition of the T4 input file
        '''
        f.write("\nCOMPOSITION\n")
        temperature = 300
        dic_composition = CIntermediateCompositionT4().m_constructCompositionT4(self.mcnp_new_dict)
        f.write(str(len(dic_composition) + 1) + "\n")
        for mat in dic_composition.values():
            s_paramMaterialComposition = ''
            l_typeDensity = mat.typeDensity
            l_densityValue = mat.valueOfDensity
            p_numberOfIsotope = mat.numberOfIsotope
            list_isotope = mat.listMaterialComposition
            for element in list_isotope:
                nameIsotope, abondanceIsotope = element
                s_paramMaterialComposition = s_paramMaterialComposition +\
                str(nameIsotope) + ' ' + str(abondanceIsotope) +' '
            for i in range(0,len(l_densityValue)):
                p_materialName = mat.material + '_' + l_densityValue[i]
                if l_typeDensity[i] == 'POINT_WISE':
                    f.write("%s %s %s %s %s \n" % (l_typeDensity[i], temperature,\
                                                  p_materialName,
                                                  p_numberOfIsotope,\
                                                  s_paramMaterialComposition))
                else:
                    f.write("%s %s %s %s %s %s \n" % (l_typeDensity[i], temperature,\
                                                  p_materialName,fabs(float(l_densityValue[i])),\
                                                  p_numberOfIsotope,\
                                                  s_paramMaterialComposition))
        f.write("POINT_WISE 300 m0 1 HE4 1E-30\n")

        f.write("\n")
        f.write("END_COMPOSITION")
        f.write("\n")


# CWriteT4Composition().m_writeT4Composition()

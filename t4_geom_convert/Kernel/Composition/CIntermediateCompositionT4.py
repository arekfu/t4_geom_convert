# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateCompositionT4.py
'''
from ..Composition.CCompositionT4 import CCompositionT4
from ..Composition.CCompositionConversionMCNPToT4 import CCompositionConversionMCNPToT4
from ..Volume.CDictCellMCNP import CDictCellMCNP

class CIntermediateCompositionT4(object):
    '''
    :brief: Intermediate class which change the value of the dictionary from the conversion in
    instance of the Class CCompositionT4
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def m_constructCompositionT4(self):
        '''
        :brief: method changing the tuple from CCompositionConversionMCNPToT4
        in instance of the CVolumeT4 Class
        '''
        dic_newCompositionT4 = dict()
        dic_CompositionT4 = CCompositionConversionMCNPToT4().m_conversionCompositionMCNPToT4()
        for key,val in dic_CompositionT4.items():
            print(key, val)
            l_listeMaterialComposition = []
            l_density = []
            l_typeDensityT4 = []
            for elmt in val:
                isotopeCaracteristic, abondance = elmt
                enumElement, massNumber = isotopeCaracteristic
                nameElement = enumElement.name
                if massNumber[0] == '0':
                    massNumber = massNumber[1:]
                isotopeT4 = nameElement + massNumber
                l_listeMaterialComposition.append((isotopeT4, abondance))
            dic_cellMCNP = CDictCellMCNP().d_cellMCNP
            for k in dic_cellMCNP.keys():
                if int(dic_cellMCNP[k].materialID) == key:
                    density = dic_cellMCNP[k].density
                    if float(density) not in l_density:
                        l_density.append(float(density))
                        if float(density) < 0:
                            l_typeDensityT4.append('DENSITY')
                        if float(density) > 0:
                            l_typeDensityT4.append('POINT_WISE')
            dic_newCompositionT4[key] = CCompositionT4(l_typeDensityT4, 'm'+str(key),\
                                                       l_density,\
                                                       len(l_listeMaterialComposition),\
                                                       l_listeMaterialComposition)
        return dic_newCompositionT4

# d = CIntermediateCompositionT4().m_constructCompositionT4()
# for keys in d.keys():
#     print(keys)
#     print(d[keys].typeDensity)

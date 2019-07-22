# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from .CCompositionT4 import CCompositionT4
from .CompositionConversionMCNPToT4 import compositionConversionMCNPToT4

from collections import OrderedDict


def constructCompositionT4(mcnpParser, dic_cellMCNP):
    '''
    :brief: method changing the tuple from compositionConversionMCNPToT4
    in instance of the CVolumeT4 Class
    '''
    dic_newCompositionT4 = OrderedDict()
    dic_CompositionT4 = compositionConversionMCNPToT4(mcnpParser)
    for key,val in dic_CompositionT4.items():
        composition = []
        l_density = []
        l_typeDensityT4 = []
        for elmt in val:
            isotopeCaracteristic, abondance = elmt
            enumElement, massNumber = isotopeCaracteristic
            nameElement = enumElement.name
            if massNumber[0] == '0':
                massNumber = massNumber[1:]
            isotopeT4 = nameElement + massNumber
            composition.append((isotopeT4, abondance))
        for cell in dic_cellMCNP.values():
            if cell.importance <= 0. or cell.universe != 0 or cell.fillid is not None:
                continue
            if int(cell.materialID) == key:
                density = cell.density
                if density not in l_density:
                    l_density.append(density)
                    if float(density) < 0:
                        l_typeDensityT4.append('DENSITY')
                    else:
                        l_typeDensityT4.append('POINT_WISE')
        dic_newCompositionT4[key] = CCompositionT4(l_typeDensityT4,
                                                    'm'+str(key), l_density,
                                                    composition)
    return dic_newCompositionT4

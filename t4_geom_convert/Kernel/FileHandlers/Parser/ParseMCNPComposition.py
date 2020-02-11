# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
'''

from collections import OrderedDict
from MIP.geom.composition import get_material_composition
from ...Composition.CCompositionMCNP import CCompositionMCNP


def parseMCNPComposition(mcnpParser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the materials as a key
    and as a value, a object from the class CCompositionMCNP
    '''
    compositionParser = get_material_composition(mcnpParser)
    dictComposition = OrderedDict()
    for k, v in list(compositionParser.items()):
        l_materialCompositionParameters = v
        dictComposition[k] = CCompositionMCNP(l_materialCompositionParameters)
    return dictComposition

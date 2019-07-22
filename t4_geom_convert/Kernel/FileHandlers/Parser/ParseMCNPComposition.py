# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
'''

from MIP.geom.grammars.composition import get_materialComposition
from ...Composition.CCompositionMCNP import CCompositionMCNP
from collections import OrderedDict


def parseMCNPComposition(mcnpParser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the materials as a key
    and as a value, a object from the class CCompositionMCNP
    '''
    compositionParser = get_materialComposition(mcnpParser, lim=None)
    dictComposition = OrderedDict()
    for k, v in list(compositionParser.items()):
        l_materialCompositionParameters = v
        dictComposition[k] = CCompositionMCNP(l_materialCompositionParameters)
    return dictComposition

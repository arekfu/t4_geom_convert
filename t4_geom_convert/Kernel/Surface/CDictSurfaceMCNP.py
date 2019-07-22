# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
'''
from collections.abc import MutableMapping
from ..FileHandlers.Parser.ParseMCNPSurface import parseMCNPSurface
from collections import OrderedDict


class CDictSurfaceMCNP(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping and
    listing surface from MCNP
    '''

    def __init__(self, mcnpParser):
        '''
        Constructor
        '''
        self.d_surfaceMCNP = parseMCNPSurface(mcnpParser)

    def __getitem__(self, key):
        return self.d_surfaceMCNP[key]

    def __setitem__(self, key, value):
        self.d_surfaceMCNP[key] = value

    def __delitem__(self, key):
        del self.d_surfaceMCNP[key]

    def __iter__(self):
        return iter(self.d_surfaceMCNP)

    def __len__(self):
        return len(self.d_surfaceMCNP)

    def __repr__(self):
        return self.d_surfaceMCNP.__repr__()

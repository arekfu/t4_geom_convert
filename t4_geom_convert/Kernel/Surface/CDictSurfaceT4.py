# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
'''
from collections.abc import MutableMapping

class CDictSurfaceT4(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping
    and listing surface converted for T4
    '''

    def __init__(self, d_surfaceT4):
        '''
        Constructor
        '''
        self.surfaceT4 = d_surfaceT4

    def __getitem__(self, key):
        return self.surfaceT4[key]

    def __setitem__(self, key, value):
        self.surfaceT4[key] = value

    def __delitem__(self, key):
        del self.surfaceT4[key]

    def __iter__(self):
        return iter(self.surfaceT4)

    def __len__(self):
        return len(self.surfaceT4)

    def __repr__(self):
        return self.surfaceT4.__repr__()

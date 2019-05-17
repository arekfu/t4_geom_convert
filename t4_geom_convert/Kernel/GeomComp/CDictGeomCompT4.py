# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : CDictGeomCompT4.py
'''
from collections.abc import MutableMapping

class CDictGeomCompT4(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping and listing
    geomcomp for T4
    '''

    def __init__(self, d_geomCompT4):
        '''
        Constructor
        '''
        self.geomCompT4 = d_geomCompT4

    def __getitem__(self, key):
        return self.geomCompT4[key]

    def __setitem__(self, key, value):
        self.geomCompT4[key] = value

    def __delitem__(self, key):
        del self.geomCompT4[key]

    def __iter__(self):
        return iter(self.geomCompT4)

    def __len__(self):
        return len(self.geomCompT4)

    def __repr__(self):
        return self.geomCompT4.__repr__()

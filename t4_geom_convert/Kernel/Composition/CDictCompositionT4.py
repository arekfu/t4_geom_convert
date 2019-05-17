# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : CDictCompositionT4.py
'''
from collections.abc import MutableMapping


class CDictCompositionT4(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping and listing material 
    composition for T4 
    '''

    def __init__(self, d_compositionT4):
        '''
        Constructor
        '''
        self.compositionT4 = d_compositionT4
        
    def __getitem__(self, key):
        return self.compositionT4[key]
    
    def __setitem__(self, key, value):
        self.compositionT4[key] = value
        
    def __delitem__(self, key):
        del self.compositionT4[key]
    
    def __iter__(self):
        return iter(self.compositionT4)
    
    def __len__(self):
        return len(self.compositionT4)
    
    def __repr__(self):
        return self.compositionT4.__repr__()

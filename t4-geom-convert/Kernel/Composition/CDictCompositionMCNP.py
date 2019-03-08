# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : CDictCompositionMCNP.py
'''
from _collections_abc import MutableMapping
from FileHanlders.Parser.CParseMCNPComposition import CParseMCNPComposition


class CDictCompositionMCNP(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping and listing material composition from MCNP 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.d_compositionMCNP = dict()
        self.d_compositionMCNP = CParseMCNPComposition().m_parsingMaterialComposition()
    
    def __getitem__(self, key):
        return self.d_compositionMCNP[key]
    
    def __setitem__(self, key, value):
        self.d_compositionMCNP[key] = value
        
    def __delitem__(self, key):
        del self.d_compositionMCNP[key]
    
    def __iter__(self):
        return iter(self.d_compositionMCNP)
    
    def __len__(self):
        return len(self.d_compositionMCNP)
    
    def __repr__(self):
        return self.d_compositionMCNP.__repr__()
    
# for key,val in CDictCompositionMCNP().d_compositionMCNP.items() :  
#     l = val.m_ordDict()
#     print(key, l)

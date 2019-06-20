# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : CUniverseDict.py
'''
from FileHanlders.Parser.CParseMCNPCell import CParseMCNPCell


class CUniverseDict(object):
    '''
    :brief: Class inheriting of abstract class MutableMapping and listing
    cell from MCNP
    '''

    def __init__(self, d_dicCellMCNP):
        '''
        Constructor
        '''
        self.d_cellMCNP = dict()
        self.d_cellMCNP = d_dicCellMCNP
    
    def m_dictUniverse(self):
        
        d_universeDict = dict()
        for k, val in self.d_cellMCNP.items():
            d_universeDict[int(val.universe)] = []
        for k, val in self.d_cellMCNP.items():
            d_universeDict[int(val.universe)].append(k)
        return d_universeDict

# p = CUniverseDict().m_dictUniverse()
# for k in p.keys():
#     print(k, p[k])
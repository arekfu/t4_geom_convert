# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : CDictCellMCNP.py
'''
from collections.abc import MutableMapping
from ..FileHandlers.Parser.CParseMCNPCell import CParseMCNPCell
from collections import OrderedDict


class CDictCellMCNP(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping and listing
    cell from MCNP
    '''

    def __init__(self, mcnpParser, cell_cache_path, lattice_params):
        '''
        Constructor
        '''
        self.d_cellMCNP = CParseMCNPCell(mcnpParser, cell_cache_path,
                                         lattice_params).parsingCell()

    def __getitem__(self, key):
        return self.d_cellMCNP[key]

    def __setitem__(self, key, value):
        self.d_cellMCNP[key] = value

    def __delitem__(self, key):
        del self.d_cellMCNP[key]

    def __iter__(self):
        return iter(self.d_cellMCNP)

    def __len__(self):
        return len(self.d_cellMCNP)

    def __repr__(self):
        return self.d_cellMCNP.__repr__()

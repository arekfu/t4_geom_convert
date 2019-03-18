# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CParseMCNPCell.py

.. doctest:: CParseMCNPCell
    :hide:
    >>> from CParseMCNPCell import CParseMCNPCell
    >>> objet_MCNPCell = CParseMCNPCell()
    >>> dict_Cell = objet_MCNPCell.m_parsingCell()
    >>> print(dict_Cell)

'''

from ....MIP.geom.cells import get_cells
from ....MIP import mip
from ....MIP.geom.parsegeom import get_ast
from .Parameters import f_inputMCNP
from ...Volume.CCellMCNP import CCellMCNP
class CParseMCNPCell(object):
    '''
    :brief: Class which parse the block CELLS.
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = f_inputMCNP
        
    def m_parsingCell(self):
        '''
        :brief method which permit to recover the information of each line of
        the block CELLS
        :return: dictionary which contains the ID of the cells as a key
        and as a value, a object from the class CCellMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        cellParser = get_cells(inputCell, lim=None)
        dictCell = dict()
        for k, v in list(cellParser.items()):
            material, geometry, option = v
            materialID = material.split()[0]
            if int(materialID) == 0:
                density = None
            else:
                density = material.split()[1]
            astMcnp = get_ast(geometry)
            importance = option
            dictCell[k] = CCellMCNP(materialID, density, astMcnp, importance)
        return dictCell

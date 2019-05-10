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
import re
from ....MIP.geom.cells import get_cells
from ....MIP import mip
from ....MIP.geom.parsegeom import get_ast
from ...Volume.CCellMCNP import CCellMCNP
from ....MIP.geom.composition import get_materialImportance
from t4_geom_convert.Kernel.Configuration.CConfigParameters import CConfigParameters
class CParseMCNPCell(object):
    '''
    :brief: Class which parse the block CELLS.
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().m_readNameMCNPInputFile()
        
    def m_parsingMaterialImportance(self):
        '''
        :brief method which permit to recover the information of each line
        of the block SURFACE
        :return: dictionary which contains the ID of the materials as a key
        and as a value, a object from the values of the importance of the cells
        '''
        inputCell = mip.MIP(self.inputMCNP)
        importanceParser = get_materialImportance(inputCell, lim=None)
        listeCellImp = []
        i = 0
        for k, v in list(importanceParser.items()):
            liste_imp = v
            for element in liste_imp:
                if 'R' in element.upper():
                    index = i
                    value_imp = liste_imp[index-1]
                    liste_findInt = re.findall(r'\d+', element)
                    numOfRep = int(liste_findInt[0])
                    listeCellImp.extend([float(value_imp)]*numOfRep)
                else:
                    listeCellImp.append(float(element))
                i += 1
        return listeCellImp

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
        liste_importance = self.m_parsingMaterialImportance()
        i = 0
        for k, v in list(cellParser.items()):
            if liste_importance[i] != 0:
                material, geometry, option = v
                materialID = material.split()[0]
                if int(materialID) == 0:
                    density = None
                else:
                    density = material.split()[1]
                astMcnp = get_ast(geometry)
                importance = option
                dictCell[k] = CCellMCNP(materialID, density, astMcnp, importance)
            i += 1
        return dictCell

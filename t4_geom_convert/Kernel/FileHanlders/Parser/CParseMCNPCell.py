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
    >>> dict_Cell = objet_MCNPCell.parsingCell()
    >>> print(dict_Cell)

'''
import re
from MIP.geom.cells import get_cells
from MIP import mip
from MIP.geom.parsegeom import get_ast
from MIP.geom.composition import get_materialImportance
from ...Volume.CCellMCNP import CCellMCNP
from ...Configuration.CConfigParameters import CConfigParameters
import pickle
from collections import OrderedDict
class CParseMCNPCell(object):
    '''
    :brief: Class which parse the block CELLS.
    '''

    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = CConfigParameters().readNameMCNPInputFile()
        
    def parsingMaterialImportance(self):
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

    def parsingCell(self):
        '''
        :brief method which permit to recover the information of each line of
        the block CELLS
        :return: dictionary which contains the ID of the cells as a key
        and as a value, a object from the class CCellMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        cellParser = get_cells(inputCell, lim=None)
        dictCell = OrderedDict()
        dicCellMCNP_name = self.inputMCNP + '_dicCellMCNP'
        try:
            with open(dicCellMCNP_name, mode='rb') as dicfile:
                dictCell = pickle.load(dicfile)
            print('jai lu le fichier')
        except:
            print('pas de fichier, je parse')
            liste_importance = self.parsingMaterialImportance()
            listeCellParser = list(cellParser.items())
            lencell = len(listeCellParser)
            for i, (k, v) in enumerate(listeCellParser):
#                 print("Parse Cell", k)
#                 print(i, '/', lencell)
                fillid = None
                costr = False
                listeparamfill = []
                importance = None
                lattice = False
                universe = 0
                material, geometry, option = v
                option_liste = option.lower().replace('(','').replace(')','').split()
                while option_liste:
                    elt = option_liste.pop(0)
                    if 'imp:n' in elt:
                        importance = float(elt.split('=')[1])
                    if ('fill=' or '*fill=') in elt:
                        if '*' in elt:
                            costr = True
                        fillid = int(float(elt.split('=')[1]))
                        while option_liste and '=' not in option_liste[0]:
                            listeparamfill.append(float(option_liste.pop(0)))
                    if 'u=' in elt:
                        universe = int(float(elt.split('=')[1]))
                    if 'lat=' in elt:
                        lattice = True
                materialID = material.split()[0]
                if int(materialID) == 0:
                    density = None
                else:
                    density = material.split()[1]
#                 print('Dens', k, density)
                astMcnp = get_ast(geometry)
                #importance = option
                if importance is None:
                    importance = liste_importance[i]
#                     print('importance',k, importance, i, liste_importance)
                if importance != 0:
                    dictCell[k] = CCellMCNP(materialID, density, astMcnp, importance, universe, fillid, listeparamfill, costr, lattice)
            with open(dicCellMCNP_name, mode='wb') as dicfile:
                pickle.dump(dictCell, dicfile)
        return dictCell
    
    def isfloat(self, value):
        try:
            float(value)
            return True
        except:
            return False

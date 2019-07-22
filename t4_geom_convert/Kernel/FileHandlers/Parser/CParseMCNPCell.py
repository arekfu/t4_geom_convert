# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
'''
import re
from MIP.geom.cells import get_cells
from MIP.geom.parsegeom import get_ast
from MIP.geom.composition import get_materialImportance
from ...Volume.CCellMCNP import CCellMCNP
import pickle
from collections import OrderedDict


class CParseMCNPCell:
    '''
    :brief: Class which parse the block CELLS.
    '''

    def __init__(self, mcnpParser, cell_cache_path):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.mcnpParser = mcnpParser
        self.cell_cache_path = cell_cache_path

    def parsingMaterialImportance(self):
        '''
        :brief method which permit to recover the information of each line
        of the block SURFACE
        :return: dictionary which contains the ID of the materials as a key
        and as a value, a object from the values of the importance of the cells
        '''
        importanceParser = get_materialImportance(self.mcnpParser, lim=None)
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
        if self.cell_cache_path is None:
            dictCell = self.do_parsing()
        else:
            try:
                with self.cell_cache_path.open('rb') as dicfile:
                    print('reading MCNP cells from file {}...'
                          .format(self.cell_cache_path.resolve()), end='')
                    dictCell = pickle.load(dicfile)
                    print(' done')
            except:
                dictCell = self.do_parsing()
                with self.cell_cache_path.open('wb') as dicfile:
                    print('writing MCNP cells to file {}...'
                          .format(self.cell_cache_path.resolve()), end='')
                    pickle.dump(dictCell, dicfile)
                    print(' done')
        return dictCell

    def do_parsing(self):
        dictCell = OrderedDict()
        cellParser = get_cells(self.mcnpParser, lim=None)
        liste_importance = self.parsingMaterialImportance()
        listeCellParser = list(cellParser.items())
        lencell = len(listeCellParser)
        fmt_string = '\rparsing MCNP cell {{:{}d}}/{}'.format(len(str(lencell)),
                                                              lencell)
        for i, (k, v) in enumerate(listeCellParser):
            print(fmt_string.format(i+1), end='', flush=True)
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
            astMcnp = get_ast(geometry)
            #importance = option
            if importance is None:
                importance = liste_importance[i]
            if importance != 0:
                dictCell[k] = CCellMCNP(materialID, density, astMcnp, importance, universe, fillid, listeparamfill, costr, lattice)
        print('... done', flush=True)
        return dictCell

    def isfloat(self, value):
        try:
            float(value)
            return True
        except:
            return False

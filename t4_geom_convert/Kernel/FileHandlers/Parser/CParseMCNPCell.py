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
from MIP.geom.transforms import get_transforms, to_cos
from ...Volume.CCellMCNP import CCellMCNP
from ...Volume.Lattice import parse_ranges, LatticeSpec
import pickle
from collections import OrderedDict


class CParseMCNPCell:
    '''
    :brief: Class which parse the block CELLS.
    '''

    def __init__(self, mcnpParser, cell_cache_path, lattice_params):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.mcnpParser = mcnpParser
        self.cell_cache_path = cell_cache_path
        self.lattice_params = lattice_params.copy()

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
        transforms = get_transforms(self.mcnpParser)
        for i, (key, v) in enumerate(listeCellParser):
            print(fmt_string.format(i+1), end='', flush=True)
            fillid_bounds = None
            fillid_universes = None
            costr = False
            costrcl = False
            listeparamfill = []
            listeparamtrcl = []
            importance = None
            lattice = False
            universe = 0
            material, geometry, option = v
            option_liste = option.lower().replace('(',' ').replace(')',' ').replace('=', ' ').split()
            while option_liste:
                elt = option_liste.pop(0)
                if 'imp:n' in elt:
                    importance = float(option_liste.pop(0))
                elif 'fill' in elt:
                    if '*' in elt:
                        costr = True
                    first_arg = option_liste.pop(0)
                    if ':' in first_arg:
                        str_bounds = [first_arg]
                        while option_liste and ':' in option_liste[0]:
                            str_bounds.append(option_liste.pop(0))
                        bounds = parse_ranges(str_bounds)
                        fill_universes = []
                        for _ in range(bounds.size()):
                            if not option_liste:
                                msg = ('expected {} universe specifications '
                                       'after FILL keyword, found {}'
                                       .format(bounds.size(),
                                               len(fill_universes)))
                                raise ValueError(msg)
                            elt = option_liste.pop(0)
                            try:
                                fill_universe = int(elt)
                            except ValueError:
                                msg = ('expected an integer in universe '
                                       'specifications, found {}'
                                       .format(elt))
                                raise ValueError(msg) from None
                            fill_universes.append(fill_universe)
                        fillid_bounds = bounds
                        fillid_universes = fill_universes
                    else:
                        fillid_universes = int(float(first_arg))
                    while option_liste and option_liste[0][0] in '0123456789.+-':
                        listeparamfill.append(float(option_liste.pop(0)))
                    # now handle the case where the number of the
                    # transformation was given instead of the transformation
                    # parameters
                    if len(listeparamfill) == 1:
                        trid = int(listeparamfill[0])
                        listeparamfill = transforms[trid]
                        # no need to apply to_cos, MIP takes care of it
                    elif len(listeparamfill) == 3:
                        listeparamfill += [1., 0., 0.,
                                           0., 1., 0.,
                                           0., 0., 1.]
                    elif costr:
                        listeparamfill[3:] = list(map(to_cos,
                                                      listeparamfill[3:]))
                elif 'lat' in elt:
                    lattice = True
                elif 'trcl' in elt:
                    if '*' in elt:
                        costrcl = True
                    while option_liste and option_liste[0][0] in '0123456789.+-':
                        listeparamtrcl.append(float(option_liste.pop(0)))
                    # now handle the case where the number of the
                    # transformation was given instead of the transformation
                    # parameters
                    if len(listeparamtrcl) == 1:
                        trid = int(listeparamtrcl[0])
                        listeparamtrcl = transforms[trid]
                        # no need to apply to_cos, MIP takes care of it
                    elif len(listeparamtrcl) == 3:
                        listeparamtrcl += [1., 0., 0.,
                                           0., 1., 0.,
                                           0., 0., 1.]
                    elif costr:
                        listeparamtrcl[3:] = list(map(to_cos,
                                                      listeparamtrcl[3:]))
                elif 'u' in elt:
                    universe = int(float(option_liste.pop(0)))
            materialID = material.split()[0]
            if int(materialID) == 0:
                density = None
            else:
                density = material.split()[1]
            astMcnp = get_ast(geometry)
            #importance = option
            if importance is None:
                importance = liste_importance[i]
            if fillid_bounds is None and fillid_universes is None:
                # case of no FILL, no LAT
                fillid = None
            elif lattice:
                # case of FILL=n and LAT=1
                if isinstance(fillid_universes, int):
                    try:
                        fillid_bounds = self.lattice_params[key]
                    except KeyError:
                        msg = ('no --lattice option provided for '
                                'lattice cell {}'.format(key))
                        raise ValueError(msg) from None
                    fillid_universes = [fillid_universes]*fillid_bounds.size()
                fillid = LatticeSpec(fillid_bounds, fillid_universes)
            else:
                # case of FILL=n without LAT=1
                assert fillid_bounds is None
                fillid = fillid_universes
            if importance != 0:
                trcl = [] if not listeparamtrcl else [tuple(listeparamtrcl)]
                dictCell[key] = CCellMCNP(materialID, density, astMcnp,
                                          importance, universe, fillid,
                                          tuple(listeparamfill), lattice,
                                          trcl)
        print('... done', flush=True)
        return dictCell

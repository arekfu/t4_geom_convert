# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
'''
import re
import pickle
from collections import OrderedDict, defaultdict

from MIP.geom.cells import get_cells
from MIP.geom.parsegeom import get_ast
from MIP.geom.composition import get_materialImportance
from MIP.geom.transforms import get_transforms, to_cos
from ...Volume.CellMCNP import CellMCNP
from ...Volume.Lattice import parse_ranges, LatticeSpec


class ParseMCNPCellError(Exception):
    '''An exception class for errors in MCNP cell parsing.'''


class MissingLatticeOptError(Exception):
    '''An exception class to raise when the ``--lattice`` option is missing.'''


class ParseMCNPCell:
    '''
    :brief: Class which parse the block CELLS.
    '''

    LIKE_RE = re.compile(r'like\s+(\d+)\s+but')

    def __init__(self, mcnp_parser, cell_cache_path, lattice_params):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.mcnp_parser = mcnp_parser
        self.cell_cache_path = cell_cache_path
        self.lattice_params = lattice_params.copy()
        self.importance_card = self.parse_importance_card()
        self.transforms = get_transforms(self.mcnp_parser)

    def parse_importance_card(self):
        '''
        :brief method which permit to recover the information of each line
        of the block SURFACE
        :return: dictionary which contains the ID of the materials as a key
        and as a value, a object from the values of the importance of the cells
        '''
        importance_parser = get_materialImportance(self.mcnp_parser, lim=None)
        list_cell_imp = []
        i = 0
        for value in importance_parser.values():
            list_imp = value
            for element in list_imp:
                if 'R' in element.upper():
                    index = i
                    value_imp = list_imp[index-1]
                    list_find_int = re.findall(r'\d+', element)
                    num_of_rep = int(list_find_int[0])
                    list_cell_imp.extend([float(value_imp)]*num_of_rep)
                else:
                    list_cell_imp.append(float(element))
                i += 1
        return list_cell_imp

    def parse(self):
        '''
        :brief method which permit to recover the information of each line of
        the block CELLS
        :return: dictionary which contains the ID of the cells as a key
        and as a value, a object from the :class:`~.CellMCNP` class.
        '''
        if self.cell_cache_path is None:
            dict_cell = self.parse_worker()
        else:
            try:
                with self.cell_cache_path.open('rb') as dicfile:
                    print('reading MCNP cells from file {}...'
                          .format(self.cell_cache_path.resolve()), end='')
                    dict_cell = pickle.load(dicfile)
                    print(' done')
            except IOError:
                dict_cell = self.parse_worker()
                with self.cell_cache_path.open('wb') as dicfile:
                    print('writing MCNP cells to file {}...'
                          .format(self.cell_cache_path.resolve()), end='')
                    pickle.dump(dict_cell, dicfile)
                    print(' done')
        return dict_cell

    def parse_worker(self):
        '''Actually parse the cells.'''
        dict_cell = OrderedDict()
        cell_parser = get_cells(self.mcnp_parser, lim=None)
        lencell = len(cell_parser)
        fmt_string = ('\rparsing MCNP cell {{:{}d}} ({{:3d}}%)'
                      .format(len(str(max(cell_parser)))))
        for rank, (key, parsed_cell) in enumerate(cell_parser.items()):
            percent = int(100.0*rank/(lencell-1)) if lencell > 1 else 100
            print(fmt_string.format(key, percent), end='', flush=True)
            lat_opt = self.lattice_params.get(key, None)

            # handle LIKE n BUT syntax
            match_like = self.LIKE_RE.search(parsed_cell[1].lower())
            while match_like:
                like_id = int(float(match_like.group(1)))
                like_cell = cell_parser[like_id]
                parsed_cell = self.apply_but(like_cell, parsed_cell[2])
                match_like = self.LIKE_RE.search(parsed_cell[1].lower())

            try:
                cell = self.parse_one_cell(rank, lat_opt, parsed_cell)
            except ParseMCNPCellError as err:
                msg = '{} (in cell {})'.format(err, key)
                raise ParseMCNPCellError(msg) from None
            except MissingLatticeOptError as err:
                msg = '{} for cell {}'.format(err, key)
                raise MissingLatticeOptError(msg) from None
            if cell is not None:
                dict_cell[key] = cell
        print('... done', flush=True)
        return dict_cell

    def parse_one_cell(self, rank, lat_opt, parsed_cell):
        '''Parse one cell, return new :class:`~.CellMCNP` object.'''
        material, geometry, option = parsed_cell

        material_id, density = self.parse_material(material)

        ast_mcnp = get_ast(geometry)

        kw_list = (option.lower().replace('(', ' ').replace(')', ' ')
                   .replace('=', ' ').split())
        kws = self.parse_keywords(kw_list)
        if kws is None:
            return None

        # replace some missing values with the defaults
        if kws['importance'] is None:
            kws['importance'] = self.importance_card[rank]
        if kws['u'] is None:
            kws['u'] = 0
        if kws['material'] is not None:
            material_id = kws['material']
        if kws['density'] is not None:
            density = kws['density']
        fillid = self.to_fillid(kws, lat_opt)
        kws['trcl'] = [] if not kws['trcl'] else [kws['trcl']]

        return CellMCNP(material_id, density, ast_mcnp, kws['importance'],
                        kws['u'], fillid, kws['f_params'], kws['lattice'],
                        kws['trcl'])

    @staticmethod
    def parse_material(material):
        '''Parse the material/density pair.'''
        material_id = material.split()[0]
        if int(material_id) == 0:
            density = None
        else:
            density = material.split()[1]
        return material_id, density

    def apply_but(self, parsed_cell, but_options):
        '''Extend the list of cell options with the BUT options.'''
        material, geometry, options = parsed_cell
        return material, geometry, (options + ' ' + but_options)

    @staticmethod
    def to_fillid(kws, lat_opt):
        '''Convert the values of the fill-related keywords into a single
        `fillid` specification.'''
        if kws['f_bounds'] is None and kws['f_univs'] is None:
            # case of no FILL, no LAT
            return None

        if kws['lattice']:
            # case of FILL=n and LAT=1 or 2
            f_univs_arg = kws['f_univs']
            if isinstance(f_univs_arg, int):
                if lat_opt is None:
                    msg = 'no --lattice option provided'
                    raise MissingLatticeOptError(msg) from None
                kws['f_bounds'] = lat_opt
                kws['f_univs'] = [f_univs_arg]*lat_opt.size()
            return LatticeSpec(kws['f_bounds'], kws['f_univs'])

        # case of FILL=n without LAT=1
        assert kws['f_bounds'] is None
        return kws['f_univs']

    def parse_keywords(self, kw_list):
        '''Parse the list of keywords following the cell definition.'''
        keywords = defaultdict(lambda: None)
        while kw_list:
            elt = kw_list.pop(0)
            if 'imp:n' in elt:
                importance = float(kw_list.pop(0))
                if importance == 0:
                    # do not parse cells with zero importance
                    return None
                keywords['importance'] = importance
            elif 'fill' in elt:
                f_bounds, f_univs, f_params = self.parse_fill_kw(elt, kw_list)
                keywords['f_bounds'] = f_bounds
                keywords['f_univs'] = f_univs
                keywords['f_params'] = f_params
            elif 'lat' in elt:
                keywords['lattice'] = self.parse_lat_kw(kw_list)
            elif 'trcl' in elt:
                keywords['trcl'] = self.parse_trcl_kw(elt, kw_list)
            elif 'u' in elt:
                keywords['u'] = int(float(kw_list.pop(0)))
            elif 'rho' in elt:
                # only relevant for LIKE n BUT cells
                keywords['density'] = kw_list.pop(0)
            elif 'mat' in elt:
                # only relevant for LIKE n BUT cells
                keywords['material'] = kw_list.pop(0)
        return keywords

    def parse_fill_kw(self, elt, kw_list):
        '''Parse the arguments of the FILL/*FILL keywords.'''
        fillid_bounds = None
        fillid_universes = None
        fill_params = []
        first_arg = kw_list.pop(0)
        if ':' in first_arg:
            str_bounds = [first_arg]
            while kw_list and ':' in kw_list[0]:
                str_bounds.append(kw_list.pop(0))
            bounds = parse_ranges(str_bounds)
            fill_universes = []
            for _ in range(bounds.size()):
                if not kw_list:
                    msg = ('expected {} universe specifications after FILL '
                           'keyword, found {}'
                           .format(bounds.size(), len(fill_universes)))
                    raise ValueError(msg)
                elt = kw_list.pop(0)
                try:
                    fill_universe = int(elt)
                except ValueError:
                    msg = ('expected an integer in universe specifications, '
                           'found {}'.format(elt))
                    raise ValueError(msg) from None
                fill_universes.append(fill_universe)
            fillid_bounds = bounds
            fillid_universes = fill_universes
        else:
            fillid_universes = int(float(first_arg))
        while kw_list and kw_list[0][0] in '0123456789.+-':
            fill_params.append(float(kw_list.pop(0)))
        # now handle the case where the number of the
        # transformation was given instead of the transformation
        # parameters
        if len(fill_params) == 1:
            trid = int(fill_params[0])
            fill_params = self.transforms[trid]
            # no need to apply to_cos, MIP takes care of it
        elif len(fill_params) == 3:
            fill_params += [1., 0., 0.,
                            0., 1., 0.,
                            0., 0., 1.]
        elif '*' in elt:
            fill_params[3:] = list(map(to_cos, fill_params[3:]))

        return fillid_bounds, fillid_universes, tuple(fill_params)

    @staticmethod
    def parse_lat_kw(kw_list):
        '''Parse the argument of the LAT keyword.'''
        lat_opt = kw_list.pop(0)
        try:
            lattice = int(lat_opt)
        except ValueError:
            msg = ('expected an integer in lattice specifications, found {}'
                   .format(lat_opt))
            raise ParseMCNPCellError(msg) from None
        if lattice not in (1, 2):
            msg = 'Invalid value for LAT option (LAT={})'.format(lattice)
            raise ParseMCNPCellError(msg)
        return lattice

    def parse_trcl_kw(self, elt, kw_list):
        '''Parse the arguments of the TRCL/*TRCL keywords.'''
        trcl_params = []
        while kw_list and kw_list[0][0] in '0123456789.+-':
            trcl_params.append(float(kw_list.pop(0)))
        # now handle the case where the number of the
        # transformation was given instead of the transformation
        # parameters
        if len(trcl_params) == 1:
            trid = int(trcl_params[0])
            trcl_params = self.transforms[trid]
            # no need to apply to_cos, MIP takes care of it
        elif len(trcl_params) == 3:
            trcl_params += [1., 0., 0.,
                            0., 1., 0.,
                            0., 0., 1.]
        elif '*' in elt:
            trcl_params[3:] = list(map(to_cos, trcl_params[3:]))
        return tuple(trcl_params)

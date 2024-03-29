# Copyright 2019-2024 French Alternative Energies and Atomic Energy Commission
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :

import re
import pickle
from collections import OrderedDict, defaultdict

import tatsu.exceptions

from MIP.geom.cells import get_cells, get_cell_importances
from MIP.geom.parsegeom import get_ast
from MIP.geom.transforms import to_cos
from MIP.mip.datacard import expand_data_card
from ...Progress import Progress
from ...Volume.CellMCNP import CellMCNP
from ...Volume.Lattice import parse_ranges, LatticeSpec
from ...Transformation.Transformation import (get_mcnp_transforms,
                                              normalize_transform)
from ...Utils import normalize_float


class ParseMCNPCellError(Exception):
    '''An exception class for errors in MCNP cell parsing.'''


class MissingLatticeOptError(Exception):
    '''An exception class to raise when the ``--lattice`` option is missing.'''


class ParseMCNPCell:
    '''Class that parses the CELLS block.'''

    LIKE_RE = re.compile(r'like\s+(\d+)\s+but')

    def __init__(self, mcnp_parser, cell_cache_path, lattice_params):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.mcnp_parser = mcnp_parser
        self.cell_cache_path = cell_cache_path
        self.lattice_params = lattice_params.copy()
        self.importances = self.parse_importance_cards()
        self.transforms = get_mcnp_transforms(self.mcnp_parser)
        for transform in self.transforms.values():
            if len(transform) == 13 and int(transform[-1]) != 1:
                raise NotImplementedError('affine transformations with m!=1 '
                                          'are not supported yet')

    def parse_importance_cards(self):
        '''Parse any importance cards and return the maximum importance value
        for each cell.

        :returns: the maximum importances.
        :rtype: list(float)
        '''
        importance_cards = get_cell_importances(self.mcnp_parser)
        if not importance_cards:
            return []
        # here all the lists, dicts, etc. have at least one element
        importances = [expand_data_card(card)[0]
                       for card in importance_cards.values()]
        lens = [len(importance) for importance in importances]
        if any(len_ != lens[0] for len_ in lens):
            diagn = ('\n'.join(f'{card}: {len_}'
                               for card, len_ in zip(importance_cards, lens)))
            msg = ('All the importance cards (`IMP:*\') must have the same '
                   f'number of elements.\n{diagn}')
            raise ParseMCNPCellError(msg)
        if len(lens) == 1:
            return importances[0]
        max_importances = [max(*values) for values in zip(*importances)]
        return max_importances

    def parse(self):
        '''
        :brief method which permit to recover the information of each line of
        the block CELLS
        :return: dictionary which contains the ID of the cells as a key
        and as a value, a object from the :class:`~.CellMCNP` class.
        '''
        if self.cell_cache_path is None:
            dict_cell, skipped_cells = self.parse_all_cells()
        else:
            try:
                with self.cell_cache_path.open('rb') as dicfile:
                    abspath = self.cell_cache_path.resolve()
                    print(f'reading MCNP cells from file {abspath}...', end='')
                    dict_cell, skipped_cells = pickle.load(dicfile)
                    print(' done')
            except IOError:
                dict_cell, skipped_cells = self.parse_all_cells()
                with self.cell_cache_path.open('wb') as dicfile:
                    abspath = self.cell_cache_path.resolve()
                    print(f'writing MCNP cells to file {abspath}...', end='')
                    pickle.dump((dict_cell, skipped_cells), dicfile)
                    print(' done')
        return dict_cell, skipped_cells

    def parse_all_cells(self):
        '''Actually parse the cells.'''
        dict_cell = OrderedDict()
        skipped_cells = []
        parsed_cells = get_cells(self.mcnp_parser, lim=None)
        with Progress('parsing MCNP cell',
                      len(parsed_cells), max(parsed_cells)) as progress:
            for rank, (key, parsed_cell) in enumerate(parsed_cells.items()):
                progress.update(rank, key)
                lat_opt = self.lattice_params.get(key, None)
                try:
                    cell = self.parse_one_cell(parsed_cells, rank, lat_opt,
                                               parsed_cell)
                except ParseMCNPCellError as err:
                    msg = f'{err} (in cell {key})'
                    raise ParseMCNPCellError(msg) from None
                except MissingLatticeOptError as err:
                    msg = f'{err} for cell {key}'
                    raise MissingLatticeOptError(msg) from None
                except tatsu.exceptions.ParseException as err:
                    msg = (f'TatSu parsing failed for cell {key}. Check the '
                           'syntax of this cell.'.format(key))
                    raise ParseMCNPCellError(msg) from err
                if cell.importance == 0:
                    skipped_cells.append(key)
                dict_cell[key] = cell
        return dict_cell, skipped_cells

    def parse_one_cell(self, parsed_cells, rank, lat_opt, parsed_cell):
        '''Handle the ``LIKE n BUT`` syntax, delegate the real parsing to
        :meth:`parse_one_cell_worker`.'''
        match_like = self.LIKE_RE.search(parsed_cell[1].lower())
        while match_like:
            like_id = int(float(match_like.group(1)))
            like_cell = parsed_cells[like_id]
            parsed_cell = self.apply_but(like_cell, parsed_cell[2])
            match_like = self.LIKE_RE.search(parsed_cell[1].lower())
        return self.parse_one_cell_worker(rank, lat_opt, parsed_cell)

    def parse_one_cell_worker(self, rank, lat_opt, parsed_cell):
        '''Parse one cell, return new :class:`~.CellMCNP` object.'''
        material, geometry, option = parsed_cell

        material_id, density = self.parse_material(material)

        ast_mcnp = get_ast(geometry)

        option = re.sub(' *: *', ':', option)
        option = (option.lower().replace('(', ' ').replace(')', ' ')
                  .replace('=', ' '))
        kw_list = list(reversed(option.split()))
        kws = self.parse_keywords(kw_list)

        # replace some missing values with the defaults
        if kws['importance'] is None:
            try:
                kws['importance'] = self.importances[rank]
            except IndexError:
                raise ParseMCNPCellError('Cannot find importance') from None
        if kws['u'] is None:
            kws['u'] = 0
        if kws['material'] is not None:
            material_id = kws['material']
        if kws['density'] is not None:
            density = normalize_float(kws['density'])
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
            density = normalize_float(material.split()[1])
        return material_id, density

    @staticmethod
    def apply_but(parsed_cell, but_options):
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
                kws['f_univs'] = [f_univs_arg] * lat_opt.size()
            return LatticeSpec(kws['f_bounds'], kws['f_univs'])

        # case of FILL=n without LAT=1
        assert kws['f_bounds'] is None
        return kws['f_univs']

    def parse_keywords(self, kw_list):
        '''Parse the list of keywords following the cell definition.'''
        keywords = defaultdict(lambda: None)
        while kw_list:
            elt = kw_list.pop()
            if elt.startswith('imp'):
                importance = float(kw_list.pop())
                if 'importance' in keywords:
                    keywords['importance'] = max(importance,
                                                 keywords['importance'])
                else:
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
                keywords['u'] = int(float(kw_list.pop()))
            elif 'rho' in elt:
                # only relevant for LIKE n BUT cells
                keywords['density'] = kw_list.pop()
            elif 'mat' in elt:
                # only relevant for LIKE n BUT cells
                keywords['material'] = kw_list.pop()
        return keywords

    def parse_fill_kw(self, elt, kw_list):
        '''Parse the arguments of the FILL and *FILL keywords.'''
        fillid_bounds = None
        fillid_u = None
        fill_params = []
        first_arg = kw_list.pop()
        if ':' in first_arg:
            str_bounds = [first_arg]
            while kw_list and ':' in kw_list[-1]:
                str_bounds.append(kw_list.pop())
            bounds = parse_ranges(str_bounds)
            try:
                fillid_u, consumed = expand_data_card(list(reversed(kw_list)),
                                                      expected=bounds.size(),
                                                      dtype='int')
            except ValueError:
                msg = (f'expected {bounds.size()} universe specifications '
                       'after FILL keyword')
                raise ParseMCNPCellError(msg) from None
            del kw_list[-consumed:]  # remove the last `consumed` elements
            fillid_bounds = bounds
        else:
            fillid_u = int(float(first_arg))
        while kw_list and kw_list[-1][0] in '0123456789.+-':
            fill_params.append(float(kw_list.pop()))
        # now handle the case where the number of the
        # transformation was given instead of the transformation
        # parameters
        if len(fill_params) == 1:
            trid = int(fill_params[0])
            fill_params = self.transforms[trid][:12]
            # no need to apply to_cos, MIP takes care of it
        elif len(fill_params) == 3:
            fill_params = [float(param) for param in fill_params[:12]]
            fill_params += [1., 0., 0.,
                            0., 1., 0.,
                            0., 0., 1.]
        elif '*' in elt:
            fill_params = [float(x) for x in fill_params]
            fill_params[3:] = list(map(to_cos, fill_params[3:12]))
            fill_params = normalize_transform(fill_params)
        elif fill_params:
            # this is the case where the transform parameters were given inline
            fill_params = normalize_transform(fill_params)


        return fillid_bounds, fillid_u, tuple(fill_params)

    @staticmethod
    def parse_lat_kw(kw_list):
        '''Parse the argument of the LAT keyword.'''
        lat_opt = kw_list.pop()
        try:
            lattice = int(lat_opt)
        except ValueError:
            msg = ('expected an integer in lattice specifications, found '
                   f'{lat_opt}')
            raise ParseMCNPCellError(msg) from None
        if lattice not in (1, 2):
            msg = f'Invalid value for LAT option (LAT={lattice})'
            raise ParseMCNPCellError(msg)
        return lattice

    def parse_trcl_kw(self, elt, kw_list):
        '''Parse the arguments of the TRCL and *TRCL keywords.'''
        trcl_params = []
        while kw_list and kw_list[-1][0] in '0123456789.+-':
            trcl_params.append(kw_list.pop())
        # now handle the case where the number of the
        # transformation was given instead of the transformation
        # parameters
        if len(trcl_params) == 1:
            trid = int(trcl_params[0])
            trcl_params = self.transforms[trid][:12]
            # no need to apply to_cos, MIP takes care of it
        elif len(trcl_params) == 3:
            trcl_params = [float(param) for param in trcl_params[:12]]
            trcl_params += [1., 0., 0.,
                            0., 1., 0.,
                            0., 0., 1.]
        elif '*' in elt:
            trcl_params = [float(x) for x in trcl_params]
            trcl_params[3:] = list(map(to_cos, trcl_params[3:12]))
        return tuple(trcl_params)

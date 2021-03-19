# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
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

from MIP.geom.semantics import GeomExpression, Surface
from MIP.geom.main import extract_surfaces_list

from .TreeFunctions import (isLeaf, isIntersection, isUnion, isSurface,
                            isCellRef, largestPureIntersectionNode)
from .VolumeT4 import VolumeT4
from .Lattice import (LatticeSpec, latticeVector, LatticeError,
                      squareLatticeBaseVectors, hexLatticeBaseVectors)
from ..Transformation.Transformation import transformation, compose_transform
from ..Surface.ConversionSurfaceMCNPToT4 import conversion_surface_params
from ..Surface.SurfaceCollection import SurfaceCollection
from .CellMCNP import CellRef
from .CellConversionError import CellConversionError


class CellConversion:
    '''Class which contains methods to convert the Cell of MCNP in T4 Volume'''

    def __init__(self, int_cell, int_surf, d_dictClassT4, d_dictSurfaceT4,
                 d_dicSurfaceMCNP, d_dicCellMCNP):
        '''
        Constructor
        :param: int_i : id of the volume created
        :param: d_dictClassT4 : dictionary filled by the methods and which
        contains volumes informations
        '''
        self.new_cell_key = int_cell
        self.new_surf_key = int_surf
        self.dic_vol_t4 = d_dictClassT4
        self.dic_surf_t4 = d_dictSurfaceT4
        self.dic_surf_mcnp = d_dicSurfaceMCNP
        self.dic_cell_mcnp = d_dicCellMCNP
        self.convert_cellref_cache = {}
        self.convert_surface_cache = {}
        self.convert_surface_rcache = {}
        self.cell_transform_cache = {}
        self.cell_transform_rcache = {}

    @staticmethod
    def conv_equa(list_surface):
        '''Method converting a list of if of surface and return a tuple with
        the informations of the volume EQUA T4'''

        minus_surfs = []
        plus_surfs = []
        seen = set()
        for elt in list_surface:
            assert isinstance(elt, int)
            if elt in seen:
                # do not emit the same surface twice
                continue
            seen.add(elt)
            if elt < 0:
                minus_surfs.append(-elt)
            elif elt > 0:
                plus_surfs.append(elt)
        return plus_surfs, minus_surfs

    @staticmethod
    def conv_intersection(*ids):
        '''Convert a T4 INTE and return a tuple with the information of the T4
        VOLUME'''
        if ids:
            return ('INTE', ids)
        return None

    @staticmethod
    def conv_union(*ids):
        '''Convert a T4 UNION and return a tuple with the information of the T4
        VOLUME'''
        if ids:
            return ('UNION', ids)
        return None

    @staticmethod
    def conv_union_helpers(*ids, union_ids):
        '''Convert a T4 UNION and return a tuple with the information of the T4
        VOLUME'''
        pluses, minuses = CellConversion.conv_equa([union_ids[0],
                                                    -union_ids[1]])
        ops = ('UNION', ids)
        return pluses, minuses, ops

    def pot_fill(self, key, dict_universe, inline_filled=False,
                 inline_filling=False):
        cell = self.dic_cell_mcnp[key]
        if cell.fillid is None:
            return [key]
        new_cells = []
        mcnp_key_filltr = cell.filltr
        universe = int(cell.fillid)
        to_process = tuple(cell
                           for element in dict_universe[universe]
                           for cell in self.pot_fill(element, dict_universe,
                                                     inline_filled,
                                                     inline_filling))
        for element in to_process:
            element_cell = self.dic_cell_mcnp[element]
            new_cell = cell.copy()
            new_cell.fillid = None
            new_cell.materialID = element_cell.materialID
            new_cell.density = element_cell.density
            new_cell.idorigin = element_cell.idorigin.copy()
            new_cell.idorigin.append((element, key))
            cache = not inline_filling
            new_elt_key = element
            # the MCNP logic seems to be that if a cell contains a FILL with a
            # transformation, then any TRCL keyword attached to the cell is
            # disregarded. This point is tested in integration tests
            # trcl_fill.imcnp and trcl_filltr.imcnp
            if mcnp_key_filltr:
                new_elt_key = self.cell_transform(new_elt_key, mcnp_key_filltr,
                                                  cache=cache)
            elif cell.trcl:
                for trcl in cell.trcl:
                    new_elt_key = self.cell_transform(new_elt_key, trcl,
                                                      cache=cache)
            if inline_filling:
                tree = self.dic_cell_mcnp[new_elt_key].geometry
                if inline_filled:
                    new_cell.geometry = ('*', cell.geometry, tree)
                else:
                    new_cell.geometry = ('*', CellRef(key), tree)
            else:
                if inline_filled:
                    new_cell.geometry = ('*', cell.geometry,
                                         CellRef(new_elt_key))
                else:
                    new_cell.geometry = ('*', CellRef(key),
                                         CellRef(new_elt_key))
            self.new_cell_key += 1
            self.dic_cell_mcnp[self.new_cell_key] = new_cell
            new_cells.append(self.new_cell_key)
        return new_cells

    def pot_flag(self, p_tree):
        '''Method that takes a tree and return a tuple of tuple with flag to
        decorate each tree in the tree.'''
        if isLeaf(p_tree):
            return p_tree
        operator, *args = p_tree
        new_args = [self.pot_flag(node) for node in args]
        self.new_cell_key += 1
        new_tree = [self.new_cell_key, operator]
        new_tree.extend(new_args)
        return new_tree

    def pot_transform(self, p_tree, p_transf):
        if not p_transf:
            return p_tree

        if not isLeaf(p_tree):
            operator, *args = p_tree
            if operator == '^':
                # complements stay complements at this stage (they will be
                # handled later)
                return p_tree

            # recursively apply the transformation to the arguments of the
            # operator
            new_args = [self.pot_transform(node, p_transf) for node in args]
            new_tree = [operator]
            new_tree.extend(new_args)
            return tuple(new_tree)

        if isCellRef(p_tree):
            new_cell_key = self.cell_transform(p_tree.cell, p_transf)
            return CellRef(new_cell_key)

        assert isSurface(p_tree)
        surfs = self.dic_surf_mcnp[abs(p_tree)]

        surf_colls = []
        mcnp_surfs = []
        for surface_object, side in surfs:
            new_mcnp_surf = transformation(p_transf, surface_object)
            mcnp_surfs.append((new_mcnp_surf, side))
            surf_coll = conversion_surface_params(p_tree, new_mcnp_surf)
            surf_colls.append((surf_coll, side))

        surf_coll = SurfaceCollection.join(surf_colls)
        for surf, _ in surf_coll.surfs[1:]:
            surf.idorigin = tuple(list(surf.idorigin) + ['aux surf'])

        self.new_surf_key += 1
        new_key = self.new_surf_key
        self.dic_surf_t4[new_key] = surf_coll
        self.dic_surf_mcnp[new_key] = mcnp_surfs

        return Surface(new_key) if p_tree >= 0 else Surface(-new_key)

    def pot_convert(self, cell, matching, union_ids):
        tup = self.pot_flag(cell.geometry)
        expanded = self.pot_expand_surfs(tup, matching)
        opt_tree = self.pot_optimise(expanded)
        if opt_tree is None:
            # the cell is empty, do not emit a converted cell
            return None
        return self.pot_to_t4_cell(opt_tree, cell.idorigin, matching,
                                   union_ids)

    def convert_surface(self, surf, idorigin):
        p_id = self.convert_surface_cache.get(surf, None)
        if p_id is not None:
            return p_id
        self.new_cell_key += 1
        p_id = self.new_cell_key
        pluses, minuses = self.conv_equa([surf])
        self.dic_vol_t4[p_id] = VolumeT4(pluses=pluses,
                                         minuses=minuses,
                                         idorigin=idorigin)
        self.convert_surface_cache[surf] = p_id
        self.convert_surface_rcache.setdefault(p_id, []).append(surf)
        return p_id

    def convert_cellref(self, cell, matching, union_ids):
        p_id = self.convert_cellref_cache.get(cell, None)
        if p_id is not None:
            return p_id
        mcnp_cell = self.dic_cell_mcnp[cell]
        p_id = self.pot_convert(mcnp_cell, matching, union_ids)
        self.convert_cellref_cache[cell] = p_id
        return p_id

    def pot_to_t4_cell(self, p_tree, idorigin, matching, union_ids):
        '''Take the tree create by :meth:`pot_flag` and fill a dictionary (of
        VolumeT4 instance).'''
        if isSurface(p_tree):
            return self.convert_surface(p_tree, idorigin)

        if isCellRef(p_tree):
            return self.convert_cellref(p_tree.cell, matching, union_ids)

        p_id, operator, *args = p_tree

        surfs = []
        cellrefs = []
        nodes = []
        for arg in args:
            if isSurface(arg):
                surfs.append(arg)
            elif isCellRef(arg):
                cellrefs.append(arg)
            else:
                nodes.append(arg)

        if operator == '*':
            pluses, minuses = self.conv_equa(surfs)

            arg_ids = [self.pot_to_t4_cell(node, idorigin, matching, union_ids)
                       for node in nodes]
            for cellref in cellrefs:
                t4_cell_id = self.convert_cellref(cellref.cell, matching,
                                                  union_ids)
                arg_ids.append(t4_cell_id)

            ops = self.conv_intersection(*arg_ids)

            self.dic_vol_t4[p_id] = VolumeT4(pluses=pluses, minuses=minuses,
                                             ops=ops, idorigin=idorigin)
            return p_id

        # here operator == ':'
        if operator != ':':
            raise CellConversionError('Converting cell with unexpected '
                                      'operator: {}'.format(operator))
        largest = largestPureIntersectionNode(args)
        if largest is None:
            arg_ids = [self.pot_to_t4_cell(arg, idorigin, matching, union_ids)
                       for arg in args if not isCellRef(arg)]
            for cellref in cellrefs:
                t4_cell_id = self.convert_cellref(cellref.cell, matching,
                                                  union_ids)
                arg_ids.append(t4_cell_id)

            pluses, minuses, ops = self.conv_union_helpers(*arg_ids,
                                                           union_ids=union_ids)
        else:
            main = args.pop(largest)
            main_id = self.pot_to_t4_cell(main, idorigin, matching, union_ids)
            pluses = self.dic_vol_t4[main_id].pluses
            minuses = self.dic_vol_t4[main_id].minuses
            arg_ids = [self.pot_to_t4_cell(arg, idorigin, matching, union_ids)
                       for arg in args]
            for cellref in cellrefs:
                t4_cell_id = self.convert_cellref(cellref.cell, matching,
                                                  union_ids)
                arg_ids.append(t4_cell_id)
            ops = self.conv_union(*arg_ids)
        self.dic_vol_t4[p_id] = VolumeT4(pluses=pluses, minuses=minuses,
                                         ops=ops, idorigin=idorigin)
        return p_id

    def pot_optimise(self, p_tree):
        '''Method that optimizes the MCNP cells.'''

        if p_tree is None or isLeaf(p_tree):
            return p_tree

        p_id, operator, *args = p_tree
        new_args = [self.pot_optimise(node) for node in args]
        if operator == '*' and any(node is None for node in new_args):
            # this cell is empty, propagate the None
            return None
        new_args = [node for node in new_args if node is not None]
        new_node = [p_id, operator]
        for node in new_args:
            if isIntersection(node) and operator == '*':
                new_node.extend(node[2:])
            elif isUnion(node) and operator == ':':
                new_node.extend(node[2:])
            else:
                new_node.append(node)

        # we check if the cell is an intersection and contains the same surface
        # with opposite signs; in that case we do not emit the cell at all,
        # because it would be empty and because TRIPOLI-4 does not like
        # surfaces to appear with both signs at the same time
        if operator != '*':
            return new_node
        pluses = {surf for surf in new_node[2:]
                  if isSurface(surf) and surf > 0}
        minuses = {-surf for surf in new_node[2:]
                   if isSurface(surf) and surf < 0}
        if pluses & minuses:
            return None

        return new_node

    def pot_expand_surfs(self, p_tree, matching):
        '''Replace collections of surfaces with ASTs representing the
        intersection/union of the collection (necessary for one-nappe cones and
        macrobodies). Also replace MCNP surface IDs with T4 surface IDs.
        '''
        if not isLeaf(p_tree):
            p_id, operator, *args = p_tree
            new_tree = [p_id, operator]
            new_tree.extend(self.pot_expand_surfs(node, matching)
                            for node in args)
            return new_tree

        if isCellRef(p_tree):
            return p_tree

        assert isSurface(p_tree)
        t4_ids = matching[abs(p_tree.surface)]

        if p_tree.sub is not None:
            if p_tree.sub > len(t4_ids):
                msg = ('found facet {0} of surface {1} in a cell definition, '
                       'but surface {1} does not have enough facets ({2})'
                       .format(p_tree.sub, p_tree.surface, len(t4_ids)))
                raise CellConversionError(msg)
            sub_surf = t4_ids[p_tree.sub - 1]
            return sub_surf if p_tree.surface > 0 else -sub_surf

        if len(t4_ids) == 1:
            surf = t4_ids[0]
            return surf if p_tree.surface > 0 else -surf

        self.new_cell_key += 1
        if p_tree.surface < 0:
            new_node = [self.new_cell_key, '*']
            new_node.extend(-surf for surf in t4_ids)
        else:
            new_node = [self.new_cell_key, ':']
            new_node.extend(surf for surf in t4_ids)
        return GeomExpression(new_node)

    def pot_complement(self, tree):
        if not isinstance(tree, (list, tuple)):
            return tree
        if tree[0] == '^':
            cell = self.dic_cell_mcnp[int(tree[1])]
            if cell.lattice is not None:
                # This is a complement of a lattice! What does that even mean
                # We return a patently empty cell, which hopefully will later
                # be optimised away by pot_optimise
                surfaces = extract_surfaces_list(cell.geometry)
                assert len(surfaces) >= 1  # otherwise things are REALLY weird
                return ['*', surfaces[0], -surfaces[0]]
            new_geom = self.pot_complement(cell.geometry)
            return new_geom.inverse()
        new_tree = [tree[0]]
        new_tree.extend(self.pot_complement(node) for node in tree[1:])
        result = GeomExpression(new_tree)
        return result

    def extract_surfaces(self, cell):
        surf_ids = extract_surfaces_list(cell.geometry)
        return [(surf.param_surface, side if surf_id > 0 else -side)
                for surf_id in surf_ids
                for surf, side in self.dic_surf_mcnp[abs(surf_id)]]

    def develop_lattice(self, key):
        cell = self.dic_cell_mcnp[key]
        if cell.lattice is None:
            return
        assert isinstance(cell.fillid, LatticeSpec)
        assert cell.lattice in (1, 2)
        surfaces = self.extract_surfaces(cell)
        try:
            if cell.lattice == 1:
                lat_base_vectors = squareLatticeBaseVectors(surfaces)
            elif cell.lattice == 2:
                lat_base_vectors = hexLatticeBaseVectors(surfaces)
        except LatticeError as err:
            raise LatticeError('{} (in cell {})'.format(err, key)) from None

        # compute the base vectors of the lattice
        domain = cell.fillid
        if len(lat_base_vectors) != len(domain.bounds):
            if len(lat_base_vectors) != domain.bounds.dims():
                msg = ('Problem of domain definition for lattice; expected {} '
                       'non-trivial bounds, got {}'
                       .format(len(lat_base_vectors), domain.bounds.dims()))
                raise LatticeError(msg)
            n_missing_bounds = len(lat_base_vectors) - len(domain.bounds)
            for i in range(n_missing_bounds):
                range_ = domain.bounds[-1 - i]
                if range_[0] != range_[1]:
                    msg = ('Problem of domain definition for lattice; '
                           'expected {} non-trivial bounds, but the {}:{} '
                           'bound is not trivial'
                           .format(len(lat_base_vectors), range_[0],
                                   range_[1]))
                    raise LatticeError(msg)

        for index, universe in domain.items():
            if universe == 0:
                continue
            transl = latticeVector(lat_base_vectors, index)
            trnsf = list(transl) + [1., 0., 0., 0., 1., 0., 0., 0., 1.]
            new_cell_key = self.cell_transform(key, trnsf, cache=False)
            new_cell = self.dic_cell_mcnp[new_cell_key]
            if universe == cell.universe:
                new_cell.fillid = None
                new_cell.materialID = cell.materialID
            else:
                new_cell.fillid = universe
            if new_cell.filltr:
                new_filltr = compose_transform(trnsf, new_cell.filltr)
            else:
                new_filltr = tuple(trnsf)
            # see self.pot_fill(): if TRCL and FILL with a transformation are
            # both applied to a cell, TRCL is disregarded
            if cell.trcl and not cell.filltr:
                for trcl in cell.trcl:
                    new_filltr = compose_transform(trcl, new_filltr)
            new_cell.filltr = new_filltr
            new_cell.lattice = None

        del self.dic_cell_mcnp[key]

    def apply_trcl(self, trcls, geometry):
        '''Apply the given coordinate transformation to the given cell AST
        (`geometry`).

        :returns: the transformed AST
        '''
        if not trcls:
            return geometry
        for trcl in trcls:
            geometry = self.pot_transform(geometry, trcl)
        return geometry

    def cell_transform(self, cell_key, transform, cache=True):
        '''Apply `transform` to `cell`, update dictionaries and return the ID
        of the new cell.'''
        if cache:
            cache_key = (cell_key, tuple(transform))
            new_key = self.cell_transform_cache.get(cache_key, None)
        else:
            new_key = None
        if new_key is not None:
            return new_key
        if not transform:
            if cache:
                self.cell_transform_cache[cache_key] = cell_key
                (self.cell_transform_rcache
                 .setdefault(cell_key, [])
                 .append(cache_key))
            return cell_key
        cell = self.dic_cell_mcnp[cell_key]
        new_cell = cell.copy()
        tree = self.pot_transform(new_cell.geometry, transform)
        new_cell.geometry = tree
        self.new_cell_key += 1
        new_key = self.new_cell_key
        self.dic_cell_mcnp[new_key] = new_cell
        if cache:
            self.cell_transform_cache[cache_key] = new_key
            (self.cell_transform_rcache
             .setdefault(new_key, []).append(cache_key))
        return new_key

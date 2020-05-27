# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CellConversion.py
'''

from MIP.geom.semantics import GeomExpression, Surface
from MIP.geom.main import extract_surfaces_list

from .TreeFunctions import (isLeaf, isIntersection, isUnion,
                            largestPureIntersectionNode)
from .VolumeT4 import VolumeT4
from .Lattice import (LatticeSpec, latticeVector, LatticeError,
                      squareLatticeBaseVectors, hexLatticeBaseVectors)
from ..Transformation.Transformation import transformation
from ..Surface.ConversionSurfaceMCNPToT4 import conversion_surface_params
from ..Surface.SurfaceCollection import SurfaceCollection
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

    def conv_intersection(self, *ids):
        '''Convert a T4 INTE and return a tuple with the information of the T4
        VOLUME'''
        return ('INTE', ids)

    def conv_union(self, *ids):
        '''Convert a T4 UNION and return a tuple with the information of the T4
        VOLUME'''
        return ('UNION', ids)

    def conv_union_helpers(self, *ids, union_ids):
        '''Convert a T4 UNION and return a tuple with the information of the T4
        VOLUME'''
        pluses, minuses = self.conv_equa([union_ids[0],
                                          -union_ids[1]])
        ops = ('UNION', ids)
        return pluses, minuses, ops

    def pot_fill(self, key, dict_universe):
        cell = self.dic_cell_mcnp[key]
        if cell.fillid is None:
            return [key]
        new_cells = []
        mcnp_key_geom = cell.geometry
        mcnp_key_filltr = cell.filltr
        universe = int(cell.fillid)
        to_process = tuple(cell
                           for element in dict_universe[universe]
                           for cell in self.pot_fill(element, dict_universe))
        for element in to_process:
            element_cell = self.dic_cell_mcnp[element]
            mcnp_element_geom = element_cell.geometry
            self.new_cell_key += 1
            new_key = self.new_cell_key
            new_cell = cell.copy()
            new_cell.fillid = None
            new_cell.materialID = element_cell.materialID
            new_cell.density = element_cell.density
            # new_trcl = element_cell.trcl.copy()
            # if cell.trcl is not None:
            #     new_trcl.extend(cell.trcl)
            # new_cell.trcl = new_trcl
            new_cell.idorigin = element_cell.idorigin.copy()
            new_cell.idorigin.append((element, key))
            del new_cell.geometry
            tree = self.pot_transform(mcnp_element_geom, mcnp_key_filltr)
            if cell.trcl:
                tree = self.apply_trcl(cell.trcl, tree)
            new_cell.geometry = ('*', mcnp_key_geom, tree)
            self.dic_cell_mcnp[new_key] = new_cell
            new_cells.append(new_key)
        return new_cells

    def pot_flag(self, p_tree):
        '''
        :brief: method which take a tree and return a tuple of tuple with flag
        to decorate each tree in the tree
        '''
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

    def pot_convert(self, p_tree, idorigin, union_ids):
        '''
        :brief: method which take the tree create by m_postOrderTraversalFlag
        and filled a dictionary (of VolumeT4 instance)
        '''
        if isLeaf(p_tree):
            self.new_cell_key += 1
            p_id = self.new_cell_key
            pluses, minuses = self.conv_equa([p_tree])
            self.dic_vol_t4[p_id] = VolumeT4(pluses=pluses, minuses=minuses,
                                             idorigin=idorigin)
            return p_id

        p_id, operator, *args = p_tree

        if operator == '*':
            surfs = []
            nodes = []
            for arg in args:
                if isLeaf(arg):
                    surfs.append(arg)
                else:
                    nodes.append(arg)
            # here we know that paramsOPER starts as ['EQUA', 'INTE', ...]
            # because operator == '*'
            if surfs:
                pluses, minuses = self.conv_equa(surfs)
                if nodes:
                    arg_ids = [self.pot_convert(node, idorigin, union_ids)
                               for node in nodes]
                    ops = self.conv_intersection(*arg_ids)
                else:
                    ops = None
            else:
                # we assume that nodes is not empty
                arg_ids = [self.pot_convert(node, idorigin, union_ids)
                           for node in nodes]
                pluses = []
                minuses = []
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
            arg_ids = [self.pot_convert(arg, idorigin, union_ids)
                       for arg in args]
            pluses, minuses, ops = self.conv_union_helpers(*arg_ids,
                                                           union_ids=union_ids)
        else:
            main = args.pop(largest)
            main_id = self.pot_convert(main, idorigin, union_ids)
            pluses = self.dic_vol_t4[main_id].pluses
            minuses = self.dic_vol_t4[main_id].minuses
            arg_ids = [self.pot_convert(arg, idorigin, union_ids)
                       for arg in args]
            ops = self.conv_union(*arg_ids)
            del self.dic_vol_t4[main_id]
        self.dic_vol_t4[p_id] = VolumeT4(pluses=pluses, minuses=minuses,
                                         ops=ops, idorigin=idorigin)
        return p_id

    def pot_optimise(self, p_tree):
        '''
        :brief: method which permit to optimize the course of the cells MCNP
        '''

        if isLeaf(p_tree):
            return p_tree

        p_id, operator, *args = p_tree
        new_args = [self.pot_optimise(node) for node in args]
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
        pluses = {surf for surf in new_node[2:] if isLeaf(surf) and surf > 0}
        minuses = {-surf for surf in new_node[2:] if isLeaf(surf) and surf < 0}
        if pluses & minuses:
            return None

        return new_node

    def pot_replace(self, p_tree, matching):
        '''Replace collections of surfaces with ASTs representing the
        intersection/union of the collection (necessary for one-nappe cones and
        macrobodies). Also replace MCNP surface IDs with T4 surface IDs.
        '''
        if not isLeaf(p_tree):
            p_id, operator, *args = p_tree
            new_tree = [p_id, operator]
            new_tree.extend(self.pot_replace(node, matching)
                            for node in args)
            return new_tree

        assert isinstance(p_tree, Surface)
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
            assert all(isinstance(k, int) for k in self.dic_cell_mcnp)
            cell = self.dic_cell_mcnp[int(tree[1])]
            new_geom = self.pot_complement(cell.geometry)
            return new_geom.inverse()
        new_tree = [tree[0]]
        for node in tree[1:]:
            new_tree.append(self.pot_complement(node))
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
        mcnp_element_geom = cell.geometry
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
                range_ = domain.bounds[-1-i]
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
            new_cell = cell.copy()
            tree = self.pot_transform(mcnp_element_geom, trnsf)
            new_cell.geometry = tree
            if universe == cell.universe:
                new_cell.fillid = None
                new_cell.materialID = cell.materialID
            else:
                new_cell.fillid = universe
            filltr = new_cell.filltr
            if filltr:
                new_filltr = tuple(x if i > 2 else x + trnsf[i]
                                   for i, x in enumerate(filltr))
            else:
                filltr = [0.0, 0.0, 0.0,
                          1.0, 0.0, 0.0,
                          0.0, 1.0, 0.0,
                          0.0, 0.0, 1.0]
                new_filltr = tuple(x if i > 2 else x + trnsf[i]
                                   for i, x in enumerate(filltr))
            new_cell.filltr = new_filltr
            new_cell.lattice = False
            self.new_cell_key += 1
            self.dic_cell_mcnp[self.new_cell_key] = new_cell
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

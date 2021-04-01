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

class CellMCNP:
    '''Class which permit to access precisely to the information of the block
    CELLS.'''

    def __init__(self, p_materialID, p_density, syntaxTreeMCNP, p_importance,
                 p_universe, fillid, filltr, lattice, trcl, idorigin=None):
        '''
        Constructor
        :param: p_materialID : identity number of the material
        :param: p_density : value of the density
        :param: syntaxTreeMCNP : abstract syntax tree of the geometry of the cell
        :param: p_importance : float number for the importance of a cell
        :param: p_universe : universe associated to the cell
        :param: fill : directive Fill of MCNP
        :param trcl: a list of transformations to apply to this cell
        '''
        self.materialID = p_materialID
        self.density = p_density
        self.geometry = syntaxTreeMCNP
        self.importance = p_importance
        self.universe = p_universe
        self.fillid = fillid
        self.filltr = filltr
        self.lattice = lattice
        self.trcl = trcl
        self.idorigin = [] if idorigin is None else idorigin.copy()

    def evaluateASTMCNP(self):
        '''Method evaluating the syntax tree of the geometry of a cell of MCNP.
        '''
        return self.geometry.evaluate()

    def inverseASTMCNP(self):
        '''Method applying the De Morgan law on a syntax tree.'''
        self.geometry = self.geometry.inverse()

    def copy(self):
        if hasattr(self.geometry, 'copy'):
            geom_copy = self.geometry.copy() 
        else:
            geom_copy = self.geometry
        return CellMCNP(self.materialID, self.density, geom_copy,
                        self.importance, self.universe, self.fillid,
                        self.filltr, self.lattice, self.trcl.copy(),
                        self.idorigin.copy())

    def __repr__(self):
        return ('CellMCNP({!r}, {!r}, {!r},\n'
                '    {!r}, {!r}, {!r},\n'
                '    {!r}, {!r}, {!r},\n'
                '    {!r})'
                .format(self.materialID, self.density, self.geometry,
                        self.importance, self.universe, self.fillid,
                        self.filltr, self.lattice, self.trcl,
                        self.idorigin))


class CellRef:
    def __init__(self, cell):
        self.cell = cell

    def __str__(self):
        return 'CellRef({})'.format(self.cell)

    def __repr__(self):
        return 'CellRef({!r})'.format(self.cell)

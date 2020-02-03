# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CellMCNP.py
'''

class CellMCNP:
    '''
    :brief: Class which permit to access precisely to the
    information of the block CELLS
    '''


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
        '''
        :brief: method evaluating the syntax tree of the geometry of a cell of MCNP.
        '''
        return self.geometry.evaluate()

    def inverseASTMCNP(self):
        '''
        :brief: method applying the De Morgan law on a syntax tree
        '''
        self.geometry = self.geometry.inverse()

    def copy(self):
        if hasattr(self.geometry , 'copy'):
            return CellMCNP(self.materialID, self.density, self.geometry.copy(), self.importance,self.universe,self.fillid, self.filltr, self.lattice, self.trcl.copy(), self.idorigin.copy())
        return CellMCNP(self.materialID, self.density, self.geometry, self.importance,self.universe,self.fillid, self.filltr, self.lattice, self.trcl.copy(), self.idorigin.copy())

    def __repr__(self):
        return ('CellMCNP({!r}, {!r}, {!r},\n'
                '    {!r}, {!r}, {!r},\n'
                '    {!r}, {!r}, {!r},\n'
                '    {!r})'
                .format(self.materialID, self.density, self.geometry,
                        self.importance, self.universe, self.fillid,
                        self.filltr, self.lattice, self.trcl,
                        self.idorigin))

# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CCellMCNP.py
'''

class CCellMCNP(object):
    '''
    :brief: Class which permit to access precisely to the
    information of the block CELLS
    '''


    def __init__(self, p_materialID, p_density, syntaxTreeMCNP,\
                 p_importance, p_universe=0, fill=None):
        '''
        Constructor
        :param: p_materialID : identity number of the material
        :param: p_density : value of the density
        :param: syntaxTreeMCNP : abstract syntax tree of the geometry of the cell
        :param: p_importance : float number for the importance of a cell
        :param: p_universe : universe associated to the cell
        :param: fill : directive Fill of MCNP
        '''
        self.materialID = p_materialID
        self.density = p_density
        self.geometry = syntaxTreeMCNP
        self.importance = p_importance
        self.universe = p_universe
        self.fill = fill

    def m_evaluateASTMCNP(self):
        '''
        :brief: method evaluating the syntax tree of the geometry of a cell of MCNP.
        '''
        return self.geometry.evaluate()

    def m_inverseASTMCNP(self):
        '''
        :brief: method applying the De Morgan law on a syntax tree
        '''
        self.geometry = self.geometry.inverse()

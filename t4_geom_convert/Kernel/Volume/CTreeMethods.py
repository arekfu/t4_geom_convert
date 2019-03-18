# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CTreeMethods.py
'''
from ...MIP import geom



class CTreeMethods(object):
    '''
    :brief: Class which contains methods to act on tree
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def m_isLeaf(self, tree):
        '''
        :brief: method which permit to know if a tree is an instance\
          of a Surface or a Geometry
        :return: a boolean.
        '''
        if isinstance(tree, geom.semantics.GeomExpression):
            return False
        elif isinstance(tree, geom.semantics.Surface):
            return True
        else:
            return False

    def m_isInterSurface(self, tree):
        '''
        :brief: method which permit to know if a tree is an intersection \
        of Surfaces
        :return: a boolean.
        '''
        if isinstance(tree, list):
            op = tree[1]
            if all(isinstance(child, geom.semantics.Surface) for\
                   child in tree[2:]) and op == '*':
                return True

        return False

# for key,val in CDictCellMCNP().d_cellMCNP.items():
#     root = val.geometry
#     tree = root
#     print(key, CTreeMethods().m_isInterSurface(tree))

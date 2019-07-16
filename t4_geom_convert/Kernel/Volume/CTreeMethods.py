# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CTreeMethods.py
'''
from MIP import geom



class CTreeMethods(object):
    '''
    :brief: Class which contains methods to act on tree
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def isLeaf(self, tree):
        '''
        :brief: method which permit to know if a tree is an instance\
          of a Surface or a Geometry
        :return: a boolean.
        '''
        if isinstance(tree, (tuple, list, geom.semantics.GeomExpression)):
            return False
        elif isinstance(tree, (int, geom.semantics.Surface)):
            return True
        else:
            return False

    def isInterSurface(self, tree):
        '''
        :brief: method which permit to know if a tree is an intersection \
        of Surfaces
        :return: a boolean.
        '''
        if isinstance(tree, (list,tuple)):
            op = tree[1]
            if all(isinstance(child, (geom.semantics.Surface, int)) for\
                   child in tree[2:]) and op == '*':
                return True

        return False

    def isIntersection(self, tree):
        '''
        :brief: method which permit to know if a node is an intersection
        :return: a boolean.
        '''
        if isinstance(tree, (list,tuple)):
            if tree[1] == '*':
                return True

        return False

    def isUnion(self, tree):
        '''
        :brief: method which permit to know if a node is a union
        :return: a boolean.
        '''
        if isinstance(tree, (list,tuple)):
            if tree[1] == ':':
                return True

        return False

# for key,val in CDictCellMCNP().d_cellMCNP.items():
#     root = val.geometry
#     tree = root
#     print(key, CTreeMethods().isInterSurface(tree))

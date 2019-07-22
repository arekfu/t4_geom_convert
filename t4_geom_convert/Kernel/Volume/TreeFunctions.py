# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : TreeFunctions.py
'''
from MIP.geom.semantics import GeomExpression, Surface


def isLeaf(tree):
    '''
    :brief: method which permit to know if a tree is an instance of a Surface
            or a Geometry
    :return: a boolean.
    '''
    if isinstance(tree, (tuple, list, GeomExpression)):
        return False
    elif isinstance(tree, (int, Surface)):
        return True
    else:
        return False

def isIntersection(tree):
    '''
    :brief: method which permit to know if a node is an intersection
    :return: a boolean.
    '''
    if isinstance(tree, (list,tuple)):
        if tree[1] == '*':
            return True

    return False

def isUnion(tree):
    '''
    :brief: method which permit to know if a node is a union
    :return: a boolean.
    '''
    if isinstance(tree, (list,tuple)):
        if tree[1] == ':':
            return True

    return False

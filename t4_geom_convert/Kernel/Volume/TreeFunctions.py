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
    if isinstance(tree, (list, tuple)):
        if tree[1] == '*':
            return True

    return False

def isUnion(tree):
    '''
    :brief: method which permit to know if a node is a union
    :return: a boolean.
    '''
    if isinstance(tree, (list, tuple)):
        if tree[1] == ':':
            return True

    return False

def largestPureIntersectionNode(nodes):
    '''Returns the index of the largest node of the `nodes` list that is an
    intersection of surfaces, or `None` if no such node is present.

    >>> largestPureIntersectionNode([[2, '*', 1, 2], [3, '*', 4, 5, 6]])
    1
    >>> largestPureIntersectionNode([4, 5, 6])
    0
    >>> largestPureIntersectionNode([[2, '*', 1, 2],
    ...                              [3, '*', 4, 5, 6],
    ...                              [4, ':', 7, 8, 9, 10]])
    1
    >>> largestPureIntersectionNode([[3, '*', 4, 5, 6],
    ...                              [2, '*', 1, 2],
    ...                              [4, ':', 7, 8, 9, 10]])
    0
    >>> largestPureIntersectionNode([[2, ':', 1, 2], [3, ':', 4, 5, 6]])
    '''
    largest_index = None
    largest_len = 0
    for index, node in enumerate(nodes):
        if isLeaf(node) and largest_len < 1:
            largest_len = 1
            largest_index = index
            continue
        if not isinstance(node, (list, tuple)):
            continue
        if node[1] != '*':
            continue
        if not all(isLeaf(subnode) for subnode in node[2:]):
            continue
        if len(node) > largest_len:
            largest_len = len(node)
            largest_index = index
    return largest_index

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
from .CellMCNP import CellRef


def isLeaf(tree):
    '''Function which tells if a tree is an instance of a Surface or a
    Geometry.

    :rtype: bool
    '''
    if isinstance(tree, (tuple, list, GeomExpression)):
        return False
    if isinstance(tree, (int, Surface, CellRef)):
        return True
    return False


def isSurface(tree):
    '''Returns `True` if `tree` is a surface.

    :rtype: bool
    '''
    return isLeaf(tree) and isinstance(tree, (int, Surface))


def isCellRef(tree):
    '''Returns `True` if `tree` is a :class:`~.CellRef`.

    :rtype: bool
    '''
    return isLeaf(tree) and isinstance(tree, CellRef)


def isIntersection(tree):
    '''Function that tells if a node is an intersection.

    :rtype: bool
    '''
    if isinstance(tree, (list, tuple)):
        if tree[1] == '*':
            return True

    return False


def isUnion(tree):
    '''Function that tells if a node is a union.

    :rtype: bool
    '''
    if isinstance(tree, (list, tuple)):
        if tree[1] == ':':
            return True

    return False


def largestPureIntersectionNode(nodes):
    '''Returns the index of the largest node of the `nodes` list that is an
    intersection of surfaces, or `None` if no such node is present.

    >>> from .CellMCNP import CellRef
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
    >>> largestPureIntersectionNode([[3, '*', CellRef(4), 5, 6],
    ...                              [2, '*', 1, 2]])
    1
    '''
    largest_index = None
    largest_len = 0
    for index, node in enumerate(nodes):
        if isSurface(node) and largest_len < 1:
            largest_len = 1
            largest_index = index
            continue
        if not isinstance(node, (list, tuple)):
            continue
        if node[1] != '*':
            continue
        if not all(isSurface(subnode) for subnode in node[2:]):
            continue
        if len(node) > largest_len:
            largest_len = len(node)
            largest_index = index
    return largest_index

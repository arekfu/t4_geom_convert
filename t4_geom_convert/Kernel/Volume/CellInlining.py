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
'''Utilities for cell definition inlining.'''

from collections import defaultdict
from ..Progress import Progress
from .TreeFunctions import isLeaf, isCellRef, isSurface


def find_occurrences(dic):
    '''Find occurrences of inlined cells. Returns a dictionary associating
    a cell id `key` to a list of cell ids where `key` is inlined.'''
    key_stack = [key for key, value in dic.items() if value.universe == 0]
    enqueued = set(key_stack)
    occurrences = defaultdict(list)

    while key_stack:
        key = key_stack.pop()
        cell = dic[key]
        subcells = extract_subcells(cell.geometry)
        for subcell in subcells:
            occurrences[subcell].append(key)
            if subcell not in enqueued:
                key_stack.append(subcell)
                enqueued.add(subcell)

    return occurrences


def extract_subcells(geometry):
    '''Extract any subcells from the given geometry tree and return them as a
    list.

    >>> from .CellMCNP import CellRef
    >>> extract_subcells(['*', 1, 2])
    []
    >>> extract_subcells(['*', 1, CellRef(100), 2])
    [100]
    >>> extract_subcells(['*', 1, CellRef(100), [':', CellRef(5), CellRef(6)]])
    [100, 5, 6]
    '''
    if isSurface(geometry):
        return []
    _operator, *args = geometry
    subcells = []
    for arg in args:
        if isCellRef(arg):
            subcells.append(arg.cell)
        elif not isLeaf(arg):
            subcells.extend(extract_subcells(arg))
    return subcells


def compute_inlining_scores(dic, occurrences):
    '''Associate scores for inlining to each of the cells in `occurrences`. The
    lower the score, the more likely the cell is to be inlined.'''
    scores = {}
    for key, occurs in occurrences.items():
        if len(occurs) <= 1:
            # always inline cells that occur at most once
            scores[key] = 0
        else:
            scores[key] = geometry_size(dic[key].geometry) / len(occurs)
    return scores


def geometry_size(geometry):
    '''Count the number of nodes in the given geometry.

    >>> from .CellMCNP import CellRef
    >>> geometry_size(['*', 1, 2])
    2
    >>> geometry_size(['*', 1, CellRef(100), 2])
    3
    >>> geometry_size(['*', 1, CellRef(100), [':', CellRef(5), CellRef(6)]])
    4
    '''
    if isLeaf(geometry):
        return 1
    return sum(geometry_size(arg) for arg in geometry[1:])


def inline_cells(dic, max_inline_score):
    '''Perform inlining on the cells in `dic`.'''
    occurrences = find_occurrences(dic)
    if not occurrences:
        return

    # this is where we decide if we should perform any inlining
    scores = compute_inlining_scores(dic, occurrences)

    to_inline = set(key for key, score in scores.items()
                    if score < max_inline_score)

    if not to_inline:
        return

    with Progress('inlining cell definitions', len(dic), max(dic)) as progress:
        for i, (key, cell) in enumerate(dic.items()):
            progress.update(i, key)
            new_geom = inline_cells_worker(cell.geometry, dic, to_inline)
            cell.geometry = new_geom


def inline_cells_worker(geometry, dic, to_inline):
    '''Inline the cells in the `to_inline` set in `geometry`. Returns a new
    geometry.
    '''
    if isLeaf(geometry):
        return geometry
    new_geometry = [geometry[0]]
    for arg in geometry[1:]:
        if isCellRef(arg):
            if arg.cell in to_inline:
                sub_geometry = dic[arg.cell].geometry
                new_geometry.append(inline_cells_worker(sub_geometry, dic,
                                                        to_inline))
            else:
                new_geometry.append(arg)
        elif isSurface(arg):
            new_geometry.append(arg)
        else:
            new_geometry.append(inline_cells_worker(arg, dic, to_inline))
    return new_geometry

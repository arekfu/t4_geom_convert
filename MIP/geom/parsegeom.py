#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkgutil import get_data
import re
from codecs import open
import tatsu
from tatsu.ast import AST

from .semantics import GeomSemantics

from os import path


grammar = get_data('MIP.geom.grammars', 'geom.ebnf').decode('utf-8')
parser = tatsu.compile(grammar)  # , left_recurion=False)

# patterns to replace space denoting intersection with '*'
re_union = re.compile(r'\s*:\s*')
re_pareno = re.compile(r'\(\s*')
re_parenc = re.compile(r'\s*\)')
re_spaces = re.compile(r'\s+')
re_compl_cell = re.compile(r'#\s*(\d+)')
re_compl_surf = re.compile(r'#\s*\(')
re_pareno_before = re.compile(r'([^\(:^_])\(')
re_parenc_after = re.compile(r'\)([^\):^_])')


def normalize(geom):
    """Replace spaces denoting intersection with ``'*'``.

    Also replace ``'#'`` denoting surface complement with ``'_'`` and ``'#'``
    denoting cell complement with ``'^'``.
    """
    g = geom.strip()

    # remove spaces around ':' operator
    g = re_union.sub(':', g)

    # Remove spaces inside complement operators. Represent complement of
    # surfaces with _() and complement of cells with ^(). Add a space before
    # the complement operator to parse consecutive complement operators.
    g = re_compl_cell.sub(r' ^(\1)', g)
    g = re_compl_surf.sub(r' _(', g)

    # remove spaces after '(' and before ')'
    g = re_pareno.sub('(', g)
    g = re_parenc.sub(')', g)
    g = re_pareno_before.sub(r'\1 (', g)
    g = re_parenc_after.sub(r') \1', g)

    # replace one or more spaces with exactly one '*'.
    g = re_spaces.sub('*', g.strip())

    return g


def get_ast(geom):
    if 'like' in geom.lower():
        return geom.split()[1]
    g = normalize(geom)
    ast = parser.parse(g, semantics=GeomSemantics())
    return ast


def modify_ast(ast, d):
    """
    Assume ast is a recursive tuple with integers as terminal elements (signed
    surfaces).  Replace surfaces with their card representation, prepended with
    sign.
    """
    def mapping(e):
        return modify_ast(e, d)

    print('***', repr(ast))

    if isinstance(ast, tuple):
        return list(map(mapping, ast))
    elif isinstance(ast, str):
        return ast
    else:
        return ast > 0, d[abs(ast)]

    return list(map(mapping, ast))


if __name__ == '__main__':
    from sys import argv
    from mcrp_splitters import InputSplitter
    from mip.utils import shorten

    input = InputSplitter(argv[1])

    n = 0
    for c in input.cards(blocks='c', skipcomments=True):
        name, mat, geom, opts = c.parts()
        print(n, c.position, name, shorten(geom))
        ast = get_ast(geom)
        print(repr(ast))
        n += 1
        if n >= 100:
            break

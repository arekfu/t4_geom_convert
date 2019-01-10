#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import tatsu
from importlib import import_module
from os.path import basename


def pprint_dict(d, indent=4, _level=1):
    i = ' ' * indent * _level
    res = []
    # d items:
    if isinstance(d, dict):
        iterable = iter(d.items())
    elif isinstance(d, list):
        iterable = enumerate(d)
    else:
        iterable = enumerate([d])
    for k, v in iterable:
        if isinstance(v, dict) or isinstance(v, list):
            line = '{}{}:'.format(i, k)
            res.append(line)
            lines = pprint_dict(v, indent=indent, _level=_level+1)
            res.extend(lines)
        elif v is not None:
            line = '{}{}: {}'.format(i, k, v)
            res.append(line)
    return res


if __name__ == '__main__':
    from cellcard import get_cards_from_file
    from .parsegeom import normalize

    grammar = open('{}.ebnf'.format(argv[1])).read()
    parser = tatsu.compile(grammar)
    semantics = import_module('grammars.{}'.format(basename(argv[1])))


    for n, cc in get_cards_from_file(argv[2]):
        name, mat, geom, opts = cc
        if 'like' in geom.lower():
            continue
        g = normalize(geom)
        print('*'*60)
        print(repr(g))
        ast = parser.parse(g, semantics=semantics.Semantics())
        lines = pprint_dict(ast)
        print('\n'.join(lines))


# It uses the ast module from the standard library.

import ast
import re


# Convert to tuples
def convert(node):
    # Assuming that the node contains only particular types
    if isinstance(node, ast.BinOp):
        return list(map(convert, (node.op, node.left, node.right)))
    elif isinstance(node, ast.Add):
        return '+'
    elif isinstance(node, ast.Mult):
        return '*'
    elif isinstance(node, ast.Sub):
        return '-'
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Call):
        print(node._fields)
        return node._fields
    else:
        for k in node._fields:
            v = getattr(node, k)
            print(k, v)
        raise NotImplementedError('cannot convert node of type ', type(node))


def parse_cell_geom(geom):
    """
    Parse cell geometry definition geom and return
    a nested tuple of operations and operands.
    """
    r = ast.parse(geom, mode='eval').body
    return convert(r)


# patterns to replace space denoting intersection with '*'
re_union = re.compile('\s*:\s*')
re_pareno = re.compile('\(\s*')
re_parenc = re.compile('\s*\)')
re_spaces = re.compile('\s+')
re_compc = re.compile('#(\d*)')
re_comps = re.compile('#(\([^)(]*\))')


def normalize(geom):
    """
    Replace spaces denoting intersection with `*`. Replace ':' denoting union
    with '+'.

    Also replace '#' denoting complement with '_' .
    """
    g = geom.strip()
    # replace complement operator
    if '#' in g:
        g = g.replace('#', ' #')
        g = re_comps.sub(r'coms\1', g)
        g = re_compc.sub(r'comc(\1)', g)

    # remove '+', which can appear in the cell definition only as signs and
    # thus optional
    g = g.replace('+', '')
    # replae ':' with '+'
    g = re_union.sub('+', g)
    # remove spaces after '(' and before ')'
    g = re_pareno.sub('(', g)
    g = re_parenc.sub(')', g)
    # replace one or more spaces with exactly one '*'.
    g = re_spaces.sub('*', g)
    return g


if __name__ == '__main__':
    from sys import argv
    from .main import get_raw_geom

    cells, surfs, trans = get_raw_geom(argv[1])
    Nc = len(cells)
    for i, (k, v) in enumerate(cells.items()):
        print('cell {}, {}/{}'.format(k, i, Nc))
        geom = normalize(v[1])
        try:
            g = parse_cell_geom(geom)
        except Exception as e:
            print(v)
            print(geom)
            raise e

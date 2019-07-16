
"""
Geometry model is represented by two dictionaries.

One dictionary contains cells, with geometry parsed to ast.

The other dictionary contains surfaces, mentioned in the cells.
"""

from .surfaces import get_surfaces
from .cells import get_cells
from .transforms import get_transforms
from .parsegeom import get_ast
from .semantics import Surface, Cell, GeomExpression


def extract_surfaces(ast):
    """
    Return set of surfaces used in ast.
    """
    if isinstance(ast, Surface):
        return set((abs(ast), ))
    elif isinstance(ast, Cell):
        return set()

    s = set()
    if isinstance(ast[1], tuple):
        s.update(extract_surfaces(ast[1]))
    else:
        s.add(abs(ast[1]))
    if isinstance(ast[2], tuple):
        s.update(extract_surfaces(ast[2]))
    else:
        s.add(abs(ast[2]))
    return s


def extract_surfaces_list(ast):
    """
    Return set of surfaces used in ast.
    """
    if isinstance(ast, Surface):
        return [ast]
    elif isinstance(ast, Cell):
        return []

    l = []
    if isinstance(ast[1], tuple):
        l.extend(extract_surfaces_list(ast[1]))
    else:
        l.append(ast[1])
    if isinstance(ast[2], tuple):
        l.extend(extract_surfaces_list(ast[2]))
    else:
        l.append(ast[2])
    return l

def replace_surfaces(ast, dic):
    if isinstance(ast, Surface):
        surf = int(ast)
        new = dic[abs(surf)]
        return Surface(new if surf > 0 else -new)
    elif isinstance(ast, Cell):
        raise ValueError("cannot replace surfaces in #: %s" % ast)

    op, *args = ast
    l = [op]
    l.extend(replace_surfaces(arg, dic) for arg in args)
    return GeomExpression(*l)


def get_raw_geom(i, lim=None):
    if isinstance(i, str):
        from mcrp_splitters import InputSplitter
        i = InputSplitter(i)
    # read cells, surfaces and transformations from input
    cells = get_cells(i, lim=lim)
    surfs = get_surfaces(i)
    trans = get_transforms(i)
    return cells, surfs, trans


def get_geom(i, lim=None):
    cells, surfs, trans = get_raw_geom(i, lim)

    # extract only surfaces, used in cells
    used = set()
    for k, v in list(cells.items()):
        mat, geom, opts = v
        ast = get_ast(geom)
        cells[k] = ast
        used.update(extract_surfaces(ast))
    usurf = {}
    for s in used:
        usurf[s] = surfs[s]

    return cells, usurf, trans

###############################################################################
if __name__ == '__main__':
    from sys import argv
    from mcrp_splitters import InputSplitter
    from .testgrammar import pprint_dict
    from .forcad import translate

    i = InputSplitter(argv[1])
    if len(argv) >= 3:
        lim = int(argv[2])
    else:
        lim = None
    cd, sd, td = get_geom(i, lim=lim)
    cads = translate(sd, td)

    fout = open(argv[1] + '.cells', 'w')
    for k, v in list(cd.items()):
        print(k, file=fout)
        print('\n'.join(pprint_dict(v)), file=fout)
    fout.close()

    fout = open(argv[1] + '.surfaces', 'w')
    for k, v in list(sd.items()):
        print(k, file=fout)
        print('\n'.join(pprint_dict(v)), file=fout)
    fout.close()

    fout = open(argv[1] + '.transforms', 'w')
    for k, v in list(td.items()):
        print(k, file=fout)
        print(v, file=fout)  #  '\n'.join(pprint_dict(v.split()))
    fout.close()

    fout = open(argv[1] + '.cads', 'w')
    for k, v in list(cads.items()):
        print(k, file=fout)
        print('\n'.join(pprint_dict(v)), file=fout)
    fout.close()

    import json
    f = open(argv[1] + '.json', 'w')
    json.dump((cd, cads), f)


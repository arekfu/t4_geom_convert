
"""
Geometry model is represented by two dictionaries.

One dictionary contains cells, with geometry parsed to ast.

The other dictionary contains surfaces, mentioned in the cells.
"""

from surfaces import get_surfaces
from cells import get_cells
from transforms import get_transforms
from parsegeom import get_ast
from semantics import Surface, Cell


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
    for k, v in cells.items():
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
    from testgrammar import pprint_dict
    from forcad import translate

    i = InputSplitter(argv[1])
    if len(argv) >= 3:
        lim = int(argv[2])
    else:
        lim = None
    cd, sd, td = get_geom(i, lim=lim)
    cads = translate(sd, td)

    fout = open(argv[1] + '.cells', 'w')
    for k, v in cd.items():
        print >>fout, k
        print >>fout, '\n'.join(pprint_dict(v))
    fout.close()

    fout = open(argv[1] + '.surfaces', 'w')
    for k, v in sd.items():
        print >>fout, k
        print >>fout, '\n'.join(pprint_dict(v))
    fout.close()

    fout = open(argv[1] + '.transforms', 'w')
    for k, v in td.items():
        print >>fout, k
        print >>fout, v  #  '\n'.join(pprint_dict(v.split()))
    fout.close()

    fout = open(argv[1] + '.cads', 'w')
    for k, v in cads.items():
        print >>fout, k
        print >>fout, '\n'.join(pprint_dict(v))
    fout.close()

    import json
    f = open(argv[1] + '.json', 'w')
    json.dump((cd, cads), f)

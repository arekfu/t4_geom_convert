# return dictionary describing surfaces
from collections import OrderedDict

import re
re_name = re.compile('^([+*]*)(.*)')


def get_surfaces(input, lim=None):
    """
    input is an instance of mip.MIP class.
    """
    d = OrderedDict()
    n = 0
    for c in input.cards(blocks='s', skipcomments=True):
        name, tr, t, params = c.parts()
        bc, name = re_name.match(name).groups()
        name = int(name)
        t = t.strip().lower()
        params = map(float, params.split())
        d[name] = (bc, tr, t, params)
        n += 1
        if lim and n > lim:
            break
    return d


if __name__ == '__main__':
    from sys import argv
    from mcrp_splitters import InputSplitter

    i = InputSplitter(argv[1])
    d = get_surfaces(i, lim=None)
    print d.items()[0]
    print d.items()[-1]
    print len(d)

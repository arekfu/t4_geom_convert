#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from . import utils

"""
Split MCNP input file to blocks.

A working MCNP input file can have from 1 to 5 blocks:

    -------------       -----------------
    initial run         continue run
    -------------       -----------------
    message*            message*

    title               data
    cells

    surfaces

    data*
    -------------       -----------------

Also there could be situations that only part of an input file is
supplied for parsing. In this case the user must specify what block
the part starts with.

"""


class BIDClass:
    """
    BLock ID.

    Represetns block names and IDs. Only single instance is needed.
    """
    def __init__(self):
        # Order of blocks in input file:
        #   message
        #   title
        #   cells
        #   surfaces
        #   data
        self.__order = 'mtcsd'

        self.m = 0
        self.t = 1
        self.c = 2
        self.s = 3
        self.d = 4

    def __getitem__(self, i):
        return self.__order[i]


bid = BIDClass()


def get_block_positions(text, firstblock=None):
    """
    Returns a dictionary with tuple of indices that identify block start and
    end lines.
    """

    # Resulting dictionary
    dres = {}

    # Regular expresison for blank line delimiter
    bld = re.compile('^\s*$', re.MULTILINE)

    # Re.split() does not split on empty matches. Therefore, match positions
    # are searched and blocks are build manually.
    bi = []
    ps = 0  # block start position
    while ps < len(text):
        # match.start() returns index of the 1-st character of the found match,
        # in case of bld this is the next char after the 1-st \n.
        m = bld.search(text, ps)
        if m is None:
            bi.append((ps, len(text)))
            break
        pe = m.start()
        bi.append((ps, pe))
        ps = m.end() + 1

    # Line count. Starts form 1, to be consistent with vim's G
    line = 1
    # Check if message block exists
    if text[:20].split()[0].lower() == 'message:':
        dres['m'] = bi[0], line
        line += utils.nol(text, *bi[0])
        bi.pop(0)

    # Define type of the first block, if not given explicitly
    if firstblock is None:
        if len(bi) == 1:
            firstblock = bid.d
        else:
            firstblock = bid.t
            i1, i2 = utils.newlineindex(text, bi[0][0])
            bi.insert(0, (bi[0][0], i1))
            bi[1] = (i2, bi[1][1])

    cb = firstblock
    while bi:
        try:
            dres[bid[cb]] = bi[0], line
        except IndexError as err:
            raise ValueError('Cannot parse MCNP input file. Please check that '
                             'the file does not contain spurious blank lines.')
        line += utils.nol(text, *bi[0])
        bi.pop(0)
        cb += 1

    return dres


if __name__ == '__main__':
    from sys import argv
    txt = open(argv[1], 'r').read()
    d = get_block_positions(txt)
    for k, (ii, l) in list(d.items()):
        s = txt[slice(*ii)]
        print(k, l, utils.shorten(s))

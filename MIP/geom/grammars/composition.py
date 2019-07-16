# -*- coding: utf-8 -*-
'''
:author: Sogeti
:date: 07 february 2019
:file: composition.py
'''

from collections import OrderedDict

def get_materialComposition(input, lim=None):
    """
    input is an instance of mpi.MIP class.
    :brief: method to get information of material composition
    :return: a dictionary describing material composition
    """
    d = OrderedDict()
    n = 0
    #L=[]
    for c in input.cards(blocks='d', skipcomments=True):
        name, dtype, params = c.parts()
        if dtype.lower() in ('m'):
            name=int(name)
            params = params.split()
            d[name] = params
            n += 1
            if lim and n > lim:
                break
    return d


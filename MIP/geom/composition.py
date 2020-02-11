# -*- coding: utf-8 -*-
'''
:author: Sogeti
:date: 07 february 2019
:file: composition.py
'''
from collections import OrderedDict


def get_material_composition(parser):
    """Get information about material compositions.

    :param mip.MIP parser: the MIP parser.
    :returns: a dictionary describing material composition.
    """
    mat_dict = OrderedDict()
    for card in parser.cards(blocks='d', skipcomments=True):
        name, dtype, params = card.parts()
        if dtype.lower() == 'm':
            name = int(name)
            params = params.split()
            mat_dict[name] = params
    return mat_dict

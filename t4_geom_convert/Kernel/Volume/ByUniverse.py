# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : ByUniverse.py
'''
from collections import defaultdict


def by_universe(mcnp_cell_dict):
    '''Classify MCNP cells by the universe which they belong to. Return the
    classification as a dictionary associating the universe number to the list
    of cell IDs.
    '''
    universe_dict = defaultdict(list)
    for key, val in mcnp_cell_dict.items():
        universe_dict[int(val.universe)].append(key)
    return universe_dict

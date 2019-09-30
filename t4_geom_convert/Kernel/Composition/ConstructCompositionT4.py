# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from collections import OrderedDict

from .CCompositionT4 import CCompositionT4
from .CompositionConversionMCNPToT4 import compositionConversionMCNPToT4


def constructCompositionT4(mcnp_parser, dic_cell_mcnp):
    '''
    :brief: method changing the tuple from compositionConversionMCNPToT4
    in instance of the CVolumeT4 Class
    '''
    dic_new_composition_t4 = OrderedDict()
    for key, val in compositionConversionMCNPToT4(mcnp_parser).items():
        composition = []
        densities = []
        type_density_t4 = []
        for (enum_element, mass_number), abundance in val.isotopes:
            if mass_number.startswith('0'):
                # remove leading zeros
                mass_number = str(int(mass_number))
            isotope_t4 = enum_element.name + mass_number
            composition.append((isotope_t4, abundance))
        for cell in dic_cell_mcnp.values():
            if (cell.importance <= 0. or cell.universe != 0
                    or cell.fillid is not None):
                continue
            if int(cell.materialID) == key:
                density = cell.density
                if density not in densities:
                    densities.append(density)
                    if float(density) < 0:
                        type_density_t4.append('DENSITY')
                    else:
                        type_density_t4.append('POINT_WISE')
        dic_new_composition_t4[key] = CCompositionT4(type_density_t4,
                                                     'm'+str(key), densities,
                                                     composition,
                                                     val.atom_fracs)
    return dic_new_composition_t4

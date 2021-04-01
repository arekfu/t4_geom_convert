# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :

from collections import OrderedDict
from math import fsum

from .CCompositionT4 import CCompositionT4
from .CompositionConversionMCNPToT4 import compositionConversionMCNPToT4


def constructCompositionT4(mcnp_parser, dic_cell_mcnp):
    '''Function changing the tuple from compositionConversionMCNPToT4 in
    instance of the VolumeT4 class.'''
    dic_new_composition = OrderedDict()
    for key, val in compositionConversionMCNPToT4(mcnp_parser).items():
        fractions = extract_isotopes_fractions(val.isotopes)
        densities = set()
        for cell_id, cell in dic_cell_mcnp.items():
            if (cell.importance <= 0. or cell.universe != 0
                    or cell.fillid is not None):
                continue
            if int(cell.materialID) != key:
                continue
            density = cell.density
            if density in densities:
                continue
            densities.add(density)
            if float(density) < 0:
                type_density_t4 = 'DENSITY'
                compo = fractions.copy()
            else:
                # check that the composition is specified by atomic
                # fractions; mass fractions + positive concentration in
                # the cell are not supported for the moment
                type_density_t4 = 'POINT_WISE'
                if not val.atom_fracs:
                    print('\nWARNING: composition {} cannot be '
                          'correctly converted in cell {} because '
                          'total concentrations ({}) with mass '
                          'fractions are not supported at the moment'
                          .format(key, cell_id, density))
                    compo = []
                else:
                    compo = rescale_fractions(fractions, float(density))

            if key not in dic_new_composition:
                dic_new_composition[key] = []
            new_compo = CCompositionT4(type_density_t4, 'm' + str(key),
                                       density, compo, val.atom_fracs)
            dic_new_composition[key].append(new_compo)
    return dic_new_composition


def extract_isotopes_fractions(isotopes):
    '''Extract the list of isotopes and the respective fractions from the MCNP
    parsed composition.'''
    fractions = []
    for (enum_element, mass_number), abundance in isotopes:
        if mass_number.startswith('0'):
            # remove leading zeros
            mass_number = str(int(mass_number))
        isotope_t4 = enum_element.name + mass_number
        fractions.append((isotope_t4, abundance))
    return fractions


def rescale_fractions(fractions, concentration):
    '''Rescale the given atomic fractions so that the total concentration
    equals the given value.

    :param fractions: list of ``(isotope, fraction)`` pairs, as strings
    :type fractions: list((str, str))
    :param float concentration: the total concentration
    :returns: a list of ``(isotope, concentration)`` pairs, as strings
    :rtype: list((str, str))
    '''
    conc_fmt = '{:.15e}'
    concs = []
    total_fractions = fsum(float(frac) for _, frac in fractions)
    for isotope, frac in fractions:
        conc_str = conc_fmt.format(
            float(frac) * concentration / total_fractions)
        concs.append((isotope, conc_str))
    return concs

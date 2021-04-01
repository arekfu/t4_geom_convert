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

from .CDictCompositionMCNP import CDictCompositionMCNP
from .ConvertIsotope import convert_isotope
from .EIsotopeNameElementT4 import EIsotopeNameElement
from .Abundances import Abundances


def compositionConversionMCNPToT4(mcnp_parser):
    '''Function that transforms the dictionary of the composition from MCNP
    into a dictionary of the composition for T4.'''
    d_composition_t4 = OrderedDict()
    dict_compo_mcnp = CDictCompositionMCNP(mcnp_parser).d_compositionMCNP
    for key, val in dict_compo_mcnp.items():
        atom_fracs = None
        l_composition_t4 = []
        for isotope_id, fraction in val.materialCompositionParameters:
            positive_fraction = not fraction.lstrip().startswith('-')
            if atom_fracs is None:
                atom_fracs = positive_fraction
            elif positive_fraction != atom_fracs:
                raise ValueError('All isotope abundances in a material must '
                                 'have the same sign (atomic or weight '
                                 'fractions) in M{}'
                                 .format(key))

            atomic_number, mass_number = convert_isotope(isotope_id)
            atomic_number_t4 = EIsotopeNameElement(atomic_number.value)
            if mass_number == '0':
                mass_number_t4 = '-NAT'
            else:
                mass_number_t4 = mass_number
            isotope_t4 = atomic_number_t4, mass_number_t4
            l_composition_t4.append((isotope_t4, str_fabs(fraction)))
        d_composition_t4[key] = Abundances(l_composition_t4, atom_fracs)
    return d_composition_t4


def str_fabs(number_str):
    '''Remove the leading minus sign (if any) from a string representing a
    number. It behaves in a very similar way to `str(fabs(float(number_str)))`,
    except that it preserves the representation of `number_str` (precision,
    scientific notation, etc.). The input parameter must represent a valid
    float.

    :param str number_str: a number, as a string
    :returns: the absolute value of the number represented by `number_str`

    Examples:

    >>> str_fabs('-1.5')
    '1.5'
    >>> str_fabs('-1e-30')
    '1e-30'
    >>> str_fabs('-1.0e24')
    '1.0e24'
    >>> str_fabs('56.5')
    '56.5'
    >>> str_fabs('   -44  ')  # spaces are tolerated
    '44'
    '''
    number_str = number_str.strip()
    if number_str[0] == '-':
        return number_str[1:]
    return number_str

# Copyright 2019-2024 French Alternative Energies and Atomic Energy Commission
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

import re


def normalize_float(number):
    '''Return a normalized version of the given float, removing any trailing
    zeros, except one if it is the only digit after the decimal point. Also
    normalizes the Fortran scientific notation (``1.2-4 == 1.2e-4``).

    :rtype: str

    Examples:

    >>> normalize_float('1.0')
    '1.0'
    >>> normalize_float('-1')
    '-1'
    >>> normalize_float('7')
    '7'
    >>> normalize_float('1.23000')
    '1.23'
    >>> normalize_float('-1.23000')
    '-1.23'
    >>> normalize_float('-.23000')
    '-.23'
    >>> normalize_float('7')
    '7'
    >>> normalize_float('10')
    '10'
    >>> normalize_float('6.40875-2')
    '6.40875e-2'
    >>> normalize_float('6.40875+2')
    '6.40875e+2'
    >>> normalize_float('-6.40875-2')
    '-6.40875e-2'
    >>> normalize_float('-.40875-2')
    '-.40875e-2'
    >>> normalize_float('1.-2')
    '1.e-2'
    >>> normalize_float('6.3023-5')
    '6.3023e-5'
    >>> normalize_float('-5e-4')
    '-5e-4'
    >>> normalize_float('-5E-4')
    '-5e-4'
    >>> normalize_float('-5e+4')
    '-5e+4'
    >>> normalize_float('-5e4')
    '-5e4'
    >>> normalize_float('-5d4')
    '-5e4'
    '''
    norm = re.sub(r'^([-+]?[0-9]*\.[0-9]*[^0])0+$', r'\1', number)
    if norm[-1] == '.':
        norm += '0'
    norm = re.sub(r'^([-+]?([0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+))([-+][0-9]+)$',
                  r'\1e\4',
                  norm)
    norm = re.sub(r'[eEdD]', 'e', norm)
    return norm

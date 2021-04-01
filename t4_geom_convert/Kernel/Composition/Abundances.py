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
'''The module containing the :class:`Abundances` class.'''


class Abundances:  # pylint: disable=too-few-public-methods
    '''A class that represents a set of isotopes, along with their
    abundances.'''

    def __init__(self, isotopes, atom_fracs):
        '''Create a :class:`Abundances`.

        :param isotopes: the isotopes in the composition, along with their
                         abundances.
        :type isotopes: list((str, float))
        :param bool atom_fracs: `True` if the abundances represent atomic
                                fractions, `False` if they represent mass
                                fractions.
        '''
        if not isinstance(isotopes, list):
            raise ValueError('Expecting a list in Abundances, got a {}: {}'
                             .format(type(isotopes), isotopes))
        self.isotopes = isotopes.copy()
        self.atom_fracs = atom_fracs

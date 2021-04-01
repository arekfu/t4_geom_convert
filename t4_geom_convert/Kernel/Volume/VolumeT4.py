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

class VolumeT4:
    '''Class which permits to access precisely of the value of a volume T4.'''

    def __init__(self, pluses, minuses, ops=None, idorigin=None, fictive=True):
        '''
        Constructor
        '''
        self.pluses = set(pluses)
        self.minuses = set(minuses)
        self.ops = ops
        self.idorigin = idorigin.copy() if idorigin is not None else []
        self.fictive = fictive

    def __str__(self):
        str_params = ['EQUA']
        if self.pluses:
            str_params.extend(('PLUS', len(self.pluses)))
            str_params.extend(sorted(self.pluses))
        if self.minuses:
            str_params.extend(('MINUS', len(self.minuses)))
            str_params.extend(sorted(self.minuses))
        if self.ops is not None:
            str_params.extend((self.ops[0], len(self.ops[1])))
            str_params.extend(self.ops[1])
        if self.fictive:
            str_params.append('FICTIVE')
        return ' '.join(str(param) for param in str_params)

    def __repr__(self):
        return ('VolumeT4(pluses={}, minuses={}, ops={}, idorigin={}, '
                'fictive={})'.format(self.pluses, self.minuses, self.ops,
                                     self.idorigin, self.fictive))

    def copy(self):
        '''Return a copy of `self`.'''
        return VolumeT4(pluses=self.pluses.copy(), minuses=self.minuses,
                        ops=None if self.ops is None else self.ops,
                        idorigin=self.idorigin.copy(), fictive=self.fictive)

    def comment(self):
        if self.idorigin:
            return ' // ' + '; '.join(map(str, self.idorigin))
        return ''

    def empty(self):
        '''Return `True` if the cell is patently empty, i.e. if the same
        surface ID appears with opposite signs.'''
        return bool(self.pluses & self.minuses)

    def surface_ids(self):
        '''Return the surface IDs used in this volume, as a set.'''
        return self.pluses | self.minuses

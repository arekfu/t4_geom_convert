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

from collections.abc import MutableMapping


class CDictGeomCompT4(MutableMapping):
    '''Class inheriting of abstract class MutableMapping and listing geomcomp
    for T4.'''

    def __init__(self, d_geomCompT4):
        '''
        Constructor
        '''
        self.geomCompT4 = d_geomCompT4

    def __getitem__(self, key):
        return self.geomCompT4[key]

    def __setitem__(self, key, value):
        self.geomCompT4[key] = value

    def __delitem__(self, key):
        del self.geomCompT4[key]

    def __iter__(self):
        return iter(self.geomCompT4)

    def __len__(self):
        return len(self.geomCompT4)

    def __repr__(self):
        return self.geomCompT4.__repr__()

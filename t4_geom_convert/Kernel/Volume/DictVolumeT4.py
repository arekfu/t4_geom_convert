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
from collections.abc import MutableMapping


class DictVolumeT4(MutableMapping):
    '''A simple wrapper around an :class:`collections.OrderedDict` for storing
    :class:`~.VolumeT4` objects.'''

    def __init__(self):
        '''Constructor'''
        self.dict_ = OrderedDict()

    def __getitem__(self, key):
        return self.dict_[key]

    def __setitem__(self, key, value):
        self.dict_[key] = value

    def __delitem__(self, key):
        del self.dict_[key]

    def __iter__(self):
        return iter(self.dict_)

    def __len__(self):
        return len(self.dict_)

    def __repr__(self):
        return self.dict_.__repr__()

    def copy(self):
        '''Return a copy of `self`.'''
        new = DictVolumeT4()
        new.dict_ = self.dict_.copy()
        return new

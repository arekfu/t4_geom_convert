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
'''Module containing the :class:`SurfaceCollection` class.'''

from collections.abc import Sequence
from .SurfaceConversionError import SurfaceConversionError


class SurfaceCollection(Sequence):
    '''A class that represents a single surface as a collection of surfaces.

    This class is necessary to represent, for instance, MCNP's macrobodies or
    one-nappe cones.
    '''

    def __init__(self, surfs):
        '''Instantiate a :class:`SurfaceCollection`.

        :param surfs: list of (surface, side) pairs
        '''
        if not surfs:
            raise SurfaceConversionError('need a non-empty list of surfaces '
                                         'in SurfaceCollection')
        self.surfs = tuple(surfs)
        # if self.surfs[0][1] != 1:
        #     msg = ('At least one surface of the surface collection must be '
        #            'oriented in the same way as the collection itself: {}'
        #            .format(surfs))
        #     raise SurfaceConversionError(msg)

    @classmethod
    def join(cls, surf_colls):
        '''Create a :class:`SurfaceCollection` from a list of pairs of
        :class:`SurfaceCollection` objects and integers.'''
        surfs = [(sub_surf, sub_side * side)
                 for surf_coll, side in surf_colls
                 for sub_surf, sub_side in surf_coll.surfs]
        return cls(surfs)

    def __repr__(self):
        return 'SurfaceCollection({!r})'.format(self.surfs)

    def __iter__(self):
        yield from self.surfs

    def __len__(self):
        return len(self.surfs)

    def __getitem__(self, item):
        return self.surfs[item]

    def __eq__(self, other):
        return sorted(self.surfs) == sorted(other.surfs)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.surfs)

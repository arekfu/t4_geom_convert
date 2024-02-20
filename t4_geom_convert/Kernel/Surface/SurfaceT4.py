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

from itertools import chain

import numpy as np

from .ESurfaceTypeT4 import ESurfaceTypeT4 as T4S


class SurfaceT4:
    '''Class that contains the information of the TRIPOLI-4 ``SURF``
    keyword.'''

    def __init__(self, type_surface, param_surface, idorigin=None,
                 transform=None):
        '''Constructor.

        :param type_surface: string specifying the type of the Surface
        :param param_surface: list of parameters describing the surface
        :param idorigin: a list of things that describe where this surface
            comes from
        :param transform: a pair consisting of a translation vector and a
            rotation matrix to be applied to the surface
        '''

        self.type_surface = type_surface
        self.param_surface = tuple(param_surface)
        self.idorigin = idorigin if idorigin is not None else ()
        self.transform = transform

    def __str__(self):
        as_str = ' '.join(str(element)
                          for element in chain((self.type_surface.name,),
                                               self.param_surface))
        return as_str

    def __repr__(self):
        return (f'SurfaceT4({self.type_surface!r}, {self.param_surface!r}, '
                f'{self.idorigin!r}, {self.transform!r})')


    def transform_block(self):
        '''Return a string representing a coordinate transformation to be
        applied to the T4 surface, or `None` if no transformation is
        required.'''
        if self.transform is None:
            return None
        trans_params = self.transform[0].flatten('C')
        mat_params = self.transform[1].flatten('C')
        return '{} {} {} {} {} {} {} {} {} {} {} {}'.format(*trans_params,
                                                            *mat_params)


    def comment(self):
        '''Return the comment string for this surface, if any.'''
        if self.idorigin:
            return ' // ' + '; '.join(map(str, self.idorigin))
        return ''

    def __eq__(self, other):
        # idorigin intentionally omitted
        if self.transform is None:
            return (self.type_surface == other.type_surface
                    and self.param_surface == other.param_surface
                    and other.transform is None)
        if other.transform is None:
            return False
        return (self.type_surface == other.type_surface
                and self.param_surface == other.param_surface
                and np.all(self.transform[0] == other.transform[0])
                and np.all(self.transform[1] == other.transform[1]))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        # idorigin intentionally omitted
        if self.transform is None:
            return hash((self.type_surface, self.param_surface))
        return hash((self.type_surface, self.param_surface,
                     tuple(self.transform[0].flat),
                     tuple(self.transform[1].flat)))

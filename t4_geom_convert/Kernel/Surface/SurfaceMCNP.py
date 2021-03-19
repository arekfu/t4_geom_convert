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

class SurfaceMCNP:
    '''Class that contains the information of the MCNP surface cards.'''

    def __init__(self, boundary_cond, type_surface, param_surface,
                 compl_param, idorigin=None):
        '''
        Constructor
        :param boundary_cond: parameter 1 of the boundary condition
        :param type_surface: string specifying the type of the Surface
        :param param_surface: list of parameter describing the surface
        :param compl_param: list of parameter describing the surface
        :param idorigin: a list of things that describe where this surface
            comes from
        '''
        self.boundary_cond = boundary_cond
        self.type_surface = type_surface
        self.param_surface = tuple(param_surface)
        self.compl_param = tuple(compl_param)
        self.idorigin = tuple(idorigin) if idorigin is not None else ()

    def __repr__(self):
        return ('SurfaceMCNP({!r}, {!r}, {!r}, {!r}, {!r})'
                .format(self.boundary_cond, self.type_surface,
                        self.param_surface, self.compl_param, self.idorigin))

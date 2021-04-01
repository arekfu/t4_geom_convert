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

from .ConversionSurfaceMCNPToT4 import convert_mcnp_surfaces
from ..FileHandlers.Parser.ParseMCNPSurface import parseMCNPSurface


def construct_surface_t4(mcnp_parser):
    '''Method constructing a dictionary with the id of the surface as a key and
    the instance of SurfaceT4 as a value.'''
    dic_surface_mcnp = parseMCNPSurface(mcnp_parser)
    dic_surface_t4 = convert_mcnp_surfaces(dic_surface_mcnp)

    return dic_surface_t4, dic_surface_mcnp

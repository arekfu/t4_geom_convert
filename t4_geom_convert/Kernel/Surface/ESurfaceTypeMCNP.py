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

from enum import Enum

ESurfaceTypeMCNP = Enum('ESurfaceTypeMCNP', 'PX PY PZ P SO S SX SY SZ C_X '
                        'C_Y C_Z CX CY CZ C K_X K_Y K_Z KX KY KZ K SQ GQ '
                        'T TX TY TZ X Y Z '
                        # macrobody surface types
                        'BOX RPP SPH RCC HEX RHP REC TRC ELL WED ARB')


def mcnp_to_mip(en):
    if isinstance(en, str):
        s = en
    else:
        s = en.name
    return s.lower().replace('_', '/')


def string_to_enum(type_surface):
    type_surf = type_surface.upper().replace('/', '_')
    try:
        enumSurface = getattr(ESurfaceTypeMCNP, type_surf)
    except AttributeError:
        raise ValueError('{}: The type of this surface does not exist'
                         .format(type_surface.upper()))
    return enumSurface

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

from collections import defaultdict


def by_universe(mcnp_cell_dict):
    '''Classify MCNP cells by the universe which they belong to. Return the
    classification as a dictionary associating the universe number to the list
    of cell IDs.
    '''
    universe_dict = defaultdict(list)
    for key, val in mcnp_cell_dict.items():
        universe_dict[int(val.universe)].append(key)
    return universe_dict

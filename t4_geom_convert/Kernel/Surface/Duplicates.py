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
'''This module contains utilities to simplify surface dictionaries.'''

from ..Progress import Progress
from .CollectionDict import CollectionDict


def remove_duplicate_surfaces(surfs):
    '''This function that detects duplicate surfaces from a surface dictionary,
    removes them and provides a dictionary where the IDs of the deleted
    surfaces are associated with the ID of the surface that replaced them.'''
    renumbering = {}
    new_surfs = CollectionDict()
    surf_to_id = {}

    with Progress('detecting duplicates for surface',
                  len(surfs), max(surfs)) as progress:
        for i, (key, surf) in enumerate(sorted(surfs.items())):
            progress.update(i, key)
            if surf in surf_to_id:
                renumbering[key] = surf_to_id[surf]
            else:
                new_surfs[key] = surf
                renumbering[key] = key
                surf_to_id[surf] = key

    return new_surfs, renumbering


def renumber_surfaces(volus, renumbering):
    '''Apply the given surface renumbering to the volume definitions.'''
    volus = volus.copy()

    with Progress('renumbering surfaces in cell',
                  len(volus), max(volus)) as progress:
        for i, (key, volu) in enumerate(volus.items()):
            progress.update(i, key)
            new_pluses = set(renumbering[s] for s in volu.pluses)
            new_minuses = set(renumbering[s] for s in volu.minuses)
            volu.pluses = new_pluses
            volu.minuses = new_minuses
    return volus

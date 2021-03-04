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

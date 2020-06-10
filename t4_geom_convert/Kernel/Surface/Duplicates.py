'''This module contains utilities to simplify surface dictionaries.'''

from .CollectionDict import CollectionDict


def remove_duplicate_surfaces(surfs):
    '''This function that detects duplicate surfaces from a surface dictionary,
    removes them and provides a dictionary where the IDs of the deleted
    surfaces are associated with the ID of the surface that replaced them.'''
    renumbering = {}
    new_surfs = CollectionDict()
    surf_to_id = {}

    n_surfs = len(surfs)
    fmt_string = ('\rdetecting duplicates for surface {{:{0}d}} '
                  '({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                  .format(len(str(max(surfs))), len(str(n_surfs))))
    for i, (key, surf) in enumerate(sorted(surfs.items())):
        percent = int(100.0*i/(n_surfs-1)) if n_surfs > 1 else 100
        print(fmt_string.format(key, i+1, n_surfs, percent),
              end='', flush=True)
        if surf in surf_to_id:
            renumbering[key] = surf_to_id[surf]
        else:
            new_surfs[key] = surf
            renumbering[key] = key
            surf_to_id[surf] = key
    print('... done', flush=True)

    return new_surfs, renumbering


def renumber_surfaces(volus, renumbering):
    volus = volus.copy()

    n_volus = len(volus)
    fmt_string = ('\rrenumbering surfaces in cell {{:{0}d}} '
                  '({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                  .format(len(str(max(volus))), len(str(n_volus))))
    for i, (key, volu) in enumerate(volus.items()):
        percent = int(100.0*i/(n_volus-1)) if n_volus > 1 else 100
        print(fmt_string.format(key, i+1, n_volus, percent),
              end='', flush=True)
        new_pluses = set(renumbering[s] for s in volu.pluses)
        new_minuses = set(renumbering[s] for s in volu.minuses)
        volu.pluses = new_pluses
        volu.minuses = new_minuses
    print('... done', flush=True)
    return volus

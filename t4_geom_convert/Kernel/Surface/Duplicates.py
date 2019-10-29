'''This module contains utilities to simplify surface dictionaries.'''


def remove_duplicate_surfaces(surfs):
    '''This function that detects duplicate surfaces from a surface dictionary,
    removes them and provides a dictionary where the IDs of the deleted
    surfaces are associated with the ID of the surface that replaced them.'''
    renumbering = {}
    new_surfs = {}
    tuple_surf_to_id = {}

    n_surfs = len(surfs)
    fmt_string = ('\rdetecting duplicate surfaces {{:{}d}}/{} (surface {{}})'
                  .format(len(str(n_surfs)), n_surfs))
    for i, (key, (surf, fixed)) in enumerate(sorted(surfs.items())):
        print(fmt_string.format(i+1, key), end='', flush=True)
        tuple_surf = (surf.typeSurface, tuple(surf.paramSurface))
        if tuple_surf in tuple_surf_to_id:
            renumbering[key] = tuple_surf_to_id[tuple_surf]
        else:
            new_surfs[key] = (surf, fixed)
            renumbering[key] = key
            tuple_surf_to_id[tuple_surf] = key
    print('... done', flush=True)

    # renumbering fixed surfaces
    n_surfs = len(new_surfs)
    fmt_string = ('\rrenumbering fixed surfaces {{:{}d}}/{} (surface {{}})'
                  .format(len(str(n_surfs)), n_surfs))
    for i, (key, (_, fixed)) in enumerate(new_surfs.items()):
        print(fmt_string.format(i+1, key), end='', flush=True)
        for i in range(len(fixed)):
            surf = fixed[i]
            if surf > 0:
                fixed[i] = renumbering[fixed[i]]
            else:
                fixed[i] = -renumbering[-fixed[i]]
    print('... done', flush=True)

    return new_surfs, renumbering


def renumber_surfaces(volus, renumbering):
    volus = volus.copy()

    n_volus = len(volus)
    fmt_string = ('\rrenumbering surfaces in cell {{:{}d}}/{} (cell {{}})'
                  .format(len(str(n_volus)), n_volus))
    for i, (key, volu) in enumerate(volus.items()):
        print(fmt_string.format(i+1, key), end='', flush=True)
        new_pluses = set(renumbering[s] for s in volu.pluses)
        new_minuses = set(renumbering[s] for s in volu.minuses)
        volu.pluses = new_pluses
        volu.minuses = new_minuses
    print('... done', flush=True)
    return volus

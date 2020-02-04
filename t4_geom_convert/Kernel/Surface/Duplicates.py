'''This module contains utilities to simplify surface dictionaries.'''


def remove_duplicate_surfaces(surfs):
    '''This function that detects duplicate surfaces from a surface dictionary,
    removes them and provides a dictionary where the IDs of the deleted
    surfaces are associated with the ID of the surface that replaced them.'''
    renumbering = {}
    new_surfs = {}
    tuple_surf_to_id = {}

    n_surfs = len(surfs)
    fmt_string = ('\rdetecting duplicates for surface {{:{}d}} ({{:3d}}%)'
                  .format(len(str(max(surfs)))))
    for i, (key, (surf, aux)) in enumerate(sorted(surfs.items())):
        percent = int(100.0*i/(n_surfs-1)) if n_surfs > 1 else 100
        print(fmt_string.format(key, percent), end='', flush=True)
        tuple_surf = (surf.type_surface, tuple(surf.param_surface))
        if tuple_surf in tuple_surf_to_id:
            renumbering[key] = tuple_surf_to_id[tuple_surf]
        else:
            new_surfs[key] = (surf, aux)
            renumbering[key] = key
            tuple_surf_to_id[tuple_surf] = key
    print('... done', flush=True)

    # renumbering aux surfaces
    n_surfs = len(new_surfs)
    fmt_string = ('\rrenumbering auxiliary surfaces for surface {{:{}d}} '
                  '({{:3d}}%)'.format(len(str(max(new_surfs)))))
    for i, (key, (_, aux)) in enumerate(new_surfs.items()):
        percent = int(100.0*i/(n_surfs-1)) if n_surfs > 1 else 100
        print(fmt_string.format(key, percent), end='', flush=True)
        for i in range(len(aux)):
            surf = aux[i]
            if surf > 0:
                aux[i] = renumbering[aux[i]]
            else:
                aux[i] = -renumbering[-aux[i]]
    print('... done', flush=True)

    return new_surfs, renumbering


def renumber_surfaces(volus, renumbering):
    volus = volus.copy()

    n_volus = len(volus)
    fmt_string = ('\rrenumbering surfaces in cell {{:{}d}} ({{:3d}}%)'
                  .format(len(str(max(volus)))))
    for i, (key, volu) in enumerate(volus.items()):
        percent = int(100.0*i/(n_volus-1)) if n_volus > 1 else 100
        print(fmt_string.format(key, percent), end='', flush=True)
        new_pluses = set(renumbering[s] for s in volu.pluses)
        new_minuses = set(renumbering[s] for s in volu.minuses)
        volu.pluses = new_pluses
        volu.minuses = new_minuses
    print('... done', flush=True)
    return volus

# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
import pickle
from pathlib import Path

from ...Surface.ConstructSurfaceT4 import constructSurfaceT4
from ...Surface.Duplicates import remove_duplicate_surfaces, renumber_surfaces
from ...Volume.ConstructVolumeT4 import (constructVolumeT4, remove_empty_cells,
                                         extract_used_surfaces)


def writeT4Geometry(mcnpParser, lattice_params, args, ofile):
    '''
    :brief: method separated in two part,
    the first for the surface and the second for the volume
    This method fills a file of the geometry for the input file of T4
    '''
    ofile.write("GEOMETRY\n\nTITLE title\n\nHASH_TABLE\n\n")
    input_file = Path(args.input)
    t4_vol_cache_path = input_file.with_suffix('.volumes.cache')
    t4_surf_cache_path = input_file.with_suffix('.surfaces.cache')
    if args.cache:
        mcnp_cell_cache_path = input_file.with_suffix('.mcnp.cache')
    else:
        mcnp_cell_cache_path = None

    if not args.cache:
        dic_surfaceT4, dic_surfaceMCNP, aux_ids = constructSurfaceT4(mcnpParser)
    else:
        try:
            with t4_surf_cache_path.open('rb') as dicfile:
                print('reading surfaces from file {}...'
                      .format(t4_surf_cache_path.resolve()), end='', flush=True)
                dic_surfaceT4, dic_surfaceMCNP  = pickle.load(dicfile)
                print(' done', flush=True)
        except:
            dic_surfaceT4, dic_surfaceMCNP, aux_ids = constructSurfaceT4(mcnpParser)
            with t4_surf_cache_path.open('wb') as dicfile:
                print('writing surfaces to file {}...'
                      .format(t4_surf_cache_path.resolve()), end='', flush=True)
                pickle.dump((dic_surfaceT4, dic_surfaceMCNP), dicfile)
                print(' done', flush=True)

    if not args.cache:
        dic_volume, mcnp_new_dict = constructVolumeT4(mcnpParser, lattice_params, mcnp_cell_cache_path, dic_surfaceT4, dic_surfaceMCNP, aux_ids)
    else:
        try:
            with t4_vol_cache_path.open('rb') as dicfile:
                print('reading TRIPOLI-4 volumes from file {}...'
                      .format(t4_vol_cache_path.resolve()), end='', flush=True)
                dic_volume, mcnp_new_dict, dic_surfaceT4 = pickle.load(dicfile)
                print(' done', flush=True)
        except:
            dic_volume, mcnp_new_dict = constructVolumeT4(mcnpParser, lattice_params, mcnp_cell_cache_path, dic_surfaceT4, dic_surfaceMCNP, aux_ids)
            with t4_vol_cache_path.open('wb') as dicfile:
                print('writing cells to file {}...'
                      .format(t4_vol_cache_path.resolve()), end='', flush=True)
                pickle.dump((dic_volume, mcnp_new_dict, dic_surfaceT4), dicfile)
                print(' done', flush=True)

    dic_surfaceT4, surf_renumbering = remove_duplicate_surfaces(dic_surfaceT4)
    dic_volume = renumber_surfaces(dic_volume, surf_renumbering)

    remove_empty_cells(dic_volume)
    surf_used = extract_used_surfaces(dic_volume.values())

    for key in sorted(surf_used):
        surf, _ = dic_surfaceT4[key]
        list_paramSurface = surf.paramSurface
        s_paramSurface = ' '.join(str(element) for element in list_paramSurface)
        if surf.idorigin:
            s_comment = ' // ' + '; '.join(map(str, surf.idorigin))
        else:
            s_comment = ''
        ofile.write("SURF %s %s %s%s\n" % (key, surf.typeSurface.name,
                                        s_paramSurface, s_comment))
    ofile.write("\n")

    for key, val in dic_volume.items():
        ofile.write('VOLU {} {} ENDV{}\n'.format(key, val, val.comment()))
    ofile.write("\n")
    ofile.write("ENDG")
    ofile.write("\n")
    return dic_surfaceMCNP, dic_volume, mcnp_new_dict

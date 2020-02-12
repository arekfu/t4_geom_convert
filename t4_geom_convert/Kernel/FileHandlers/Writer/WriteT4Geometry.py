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
        surf_conv = constructSurfaceT4(mcnpParser)
    else:
        try:
            with t4_surf_cache_path.open('rb') as dicfile:
                print('reading surfaces from file {}...'
                      .format(t4_surf_cache_path.resolve()), end='', flush=True)
                surf_conv = pickle.load(dicfile)
                print(' done', flush=True)
        except:
            surf_conv = constructSurfaceT4(mcnpParser)
            with t4_surf_cache_path.open('wb') as dicfile:
                print('writing surfaces to file {}...'
                      .format(t4_surf_cache_path.resolve()), end='', flush=True)
                pickle.dump(surf_conv, dicfile)
                print(' done', flush=True)
    dic_surface_t4, dic_surfaceMCNP, union_ids = surf_conv

    if not args.cache:
        vol_conv = constructVolumeT4(mcnpParser, lattice_params,
                                     mcnp_cell_cache_path,
                                     dic_surface_t4,
                                     dic_surfaceMCNP, union_ids)
    else:
        try:
            with t4_vol_cache_path.open('rb') as dicfile:
                print('reading TRIPOLI-4 volumes from file {}...'
                      .format(t4_vol_cache_path.resolve()), end='', flush=True)
                vol_conv = pickle.load(dicfile)
                print(' done', flush=True)
        except:
            vol_conv = constructVolumeT4(mcnpParser, lattice_params,
                                         mcnp_cell_cache_path,
                                         dic_surface_t4,
                                         dic_surfaceMCNP, union_ids)
            with t4_vol_cache_path.open('wb') as dicfile:
                print('writing cells to file {}...'
                      .format(t4_vol_cache_path.resolve()), end='', flush=True)
                pickle.dump(vol_conv, dicfile)
                print(' done', flush=True)

    dic_volume, mcnp_new_dict, dic_surface_t4, skipped_cells = vol_conv
    dic_surface_t4, surf_renumbering = remove_duplicate_surfaces(dic_surface_t4)
    dic_volume = renumber_surfaces(dic_volume, surf_renumbering)

    remove_empty_cells(dic_volume)
    surf_used = extract_used_surfaces(dic_volume.values())

    for key in sorted(surf_used):
        surf, _ = dic_surface_t4[key]
        ofile.write("SURF {} {}{}\n".format(key, surf, surf.comment()))
    ofile.write("\n")

    for key, val in dic_volume.items():
        ofile.write('VOLU {} {} ENDV{}\n'.format(key, val, val.comment()))
    ofile.write("\n")
    ofile.write("ENDG")
    ofile.write("\n")
    return dic_surfaceMCNP, dic_volume, mcnp_new_dict, skipped_cells

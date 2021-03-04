# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
import pickle
from pathlib import Path

from ...Progress import Progress
from ...Surface.ConstructSurfaceT4 import construct_surface_t4
from ...Surface.Duplicates import remove_duplicate_surfaces, renumber_surfaces
from ...Volume.ConstructVolumeT4 import (construct_volume_t4,
                                         remove_empty_volumes,
                                         remove_unused_volumes,
                                         extract_used_surfaces)


def convertMCNPGeometry(mcnpParser, lattice_params, args):
    '''Convert an MCNP geometry to T4.'''
    input_file = Path(args.input)
    t4_vol_cache_path = input_file.with_suffix('.volumes.cache')
    t4_surf_cache_path = input_file.with_suffix('.surfaces.cache')
    if args.cache:
        mcnp_cell_cache_path = input_file.with_suffix('.mcnp.cache')
    else:
        mcnp_cell_cache_path = None

    if not args.cache:
        surf_conv = construct_surface_t4(mcnpParser)
    else:
        try:
            with t4_surf_cache_path.open('rb') as dicfile:
                print('reading surfaces from file {}...'
                      .format(t4_surf_cache_path.resolve()), end='',
                      flush=True)
                surf_conv = pickle.load(dicfile)
                print(' done', flush=True)
        except:
            surf_conv = constructSurfaceT4(mcnpParser)
            with t4_surf_cache_path.open('wb') as dicfile:
                print('writing surfaces to file {}...'
                      .format(t4_surf_cache_path.resolve()), end='',
                      flush=True)
                pickle.dump(surf_conv, dicfile)
                print(' done', flush=True)
    dic_surface_t4, dic_surface_mcnp = surf_conv

    if not args.cache:
        vol_conv = construct_volume_t4(mcnpParser, lattice_params,
                                       mcnp_cell_cache_path,
                                       dic_surface_t4,
                                       dic_surface_mcnp)
    else:
        try:
            with t4_vol_cache_path.open('rb') as dicfile:
                print('reading TRIPOLI-4 volumes from file {}...'
                      .format(t4_vol_cache_path.resolve()), end='', flush=True)
                vol_conv = pickle.load(dicfile)
                print(' done', flush=True)
        except:
            vol_conv = construct_volume_t4(mcnpParser, lattice_params,
                                           mcnp_cell_cache_path,
                                           dic_surface_t4,
                                           dic_surface_mcnp)
            with t4_vol_cache_path.open('wb') as dicfile:
                print('writing cells to file {}...'
                      .format(t4_vol_cache_path.resolve()), end='', flush=True)
                pickle.dump(vol_conv, dicfile)
                print(' done', flush=True)

    dic_volume, mcnp_new_dict, dic_surface_t4, skipped_cells = vol_conv
    if not args.skip_deduplication:
        dic_surface_t4, renumber = remove_duplicate_surfaces(dic_surface_t4)
        dic_volume = renumber_surfaces(dic_volume, renumber)

    remove_empty_volumes(dic_volume)
    remove_unused_volumes(dic_volume)

    return (dic_surface_mcnp, dic_surface_t4, dic_volume, mcnp_new_dict,
            skipped_cells)


def writeT4Geometry(dic_surface_t4, dic_volume, skipped_cells, ofile):
    '''Write out a T4 geometry to the given file. '''

    surf_used = extract_used_surfaces(dic_volume.values())
    with Progress('writing out surface',
                  len(surf_used), max(surf_used)) as progress:
        ofile.write("GEOMETRY\n\nTITLE title\n\nHASH_TABLE\n\n")
        for i, key in enumerate(sorted(surf_used)):
            progress.update(i, key)
            surf = dic_surface_t4[key]
            ofile.write("SURF {} {}{}\n".format(key, surf, surf.comment()))
        ofile.write("\n")

    with Progress('writing out volume',
                  len(dic_volume), max(dic_volume)) as progress:
        for i, (key, val) in enumerate(dic_volume.items()):
            progress.update(i, key)
            if key in skipped_cells:
                continue
            ofile.write('VOLU {} {} ENDV{}\n'.format(key, val, val.comment()))
    ofile.write("\n")
    ofile.write("ENDG")
    ofile.write("\n")

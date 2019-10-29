# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''

from collections import OrderedDict
from .CDictVolumeT4 import CDictVolumeT4
from .CDictCellMCNP import CDictCellMCNP
from .CCellConversion import CCellConversion
from .TreeFunctions import isLeaf
from .ByUniverse import by_universe


def constructVolumeT4(mcnpParser, lattice_params, cell_cache_path, dic_surface,
                      dic_surfaceMCNP, aux_ids):
    '''
    :brief: method changing the tuple from CCellConversion in
    instance of the CVolumeT4 Class
    '''
    dic_cellT4 = OrderedDict()
    objT4 = CDictVolumeT4(dic_cellT4)
    mcnp_dict = CDictCellMCNP(mcnpParser, cell_cache_path, lattice_params).d_cellMCNP

    free_key = max(int(k) for k in mcnp_dict) + 1
    free_surf_key = max(
        max(int(k) for k in dic_surfaceMCNP) + 1,
        max(int(k) for k in dic_surface) + 1
        )
    conv = CCellConversion(free_key, free_surf_key, objT4, dic_surface, dic_surfaceMCNP, mcnp_dict, aux_ids)

    # treat TRCL
    trcl_keys = [key for key, value in mcnp_dict.items()
                 if value.trcl is not None]
    if trcl_keys:
        n_trcl_keys = len(trcl_keys)
        fmt_string = ('\rapplying TRCL transformation {{:{}d}}/{} (cell {{}})'
                      .format(len(str(n_trcl_keys)), n_trcl_keys))
        for i, key in enumerate(trcl_keys):
            print(fmt_string.format(i+1, key), end='', flush=True)
            cell = mcnp_dict[key]
            cell.geometry = conv.applyTRCL(cell.trcl, cell.geometry)
            mcnp_dict[key] = cell
        print('... done', flush=True)

    n_compl = len(mcnp_dict)
    fmt_string = ('\rconverting complement {{:{}d}}/{}'
                  .format(len(str(n_compl)), n_compl))
    for i, key in enumerate(mcnp_dict):
        print(fmt_string.format(i+1), end='', flush=True)
        new_geom = conv.postOrderTraversalCompl(mcnp_dict[key].geometry)
        mcnp_dict[key].geometry = new_geom
    print('... done', flush=True)

    # treat LAT
    lat_cells = [key for key, value in mcnp_dict.items() if value.lattice]
    if lat_cells:
        n_lat_cells = len(lat_cells)
        fmt_string = ('\rdeveloping lattice {{:{}d}}/{} (cell {{}})'
                    .format(len(str(n_lat_cells)), n_lat_cells))
        for i, key in enumerate(lat_cells):
            print(fmt_string.format(i+1, key), end='', flush=True)
            conv.developLattice(key)
        print('... done', flush=True)

    # update volume and surface free keys
    conv.new_cell_key = max(int(k) for k in mcnp_dict) + 1
    conv.new_surf_key = max(
        max(int(k) for k in dic_surfaceMCNP) + 1,
        max(int(k) for k in dic_surface) + 1
        )

    # treat FILL
    dict_universe = by_universe(mcnp_dict)
    fill_keys = [key for key, value in mcnp_dict.items()
                 if value.fillid is not None]
    if fill_keys:
        n_fill_keys = len(fill_keys)
        fmt_string = ('\rdeveloping fill {{:{}d}}/{} (cell {{}})'
                    .format(len(str(n_fill_keys)), n_fill_keys))
        for i, key in enumerate(fill_keys):
            print(fmt_string.format(i+1, key), end='', flush=True)
            conv.postOrderTraversalFill(key, dict_universe)
        print('... done', flush=True)

    # update volume and surface free keys
    conv.new_cell_key = max(int(k) for k in mcnp_dict) + 1
    conv.new_surf_key = max(
        max(int(k) for k in dic_surfaceMCNP) + 1,
        max(int(k) for k in dic_surface) + 1
        )

    conv_keys = [(key, value) for key, value in mcnp_dict.items()
                 if value.importance != 0 and value.universe == 0
                 and value.fillid is None]
    n_conv_keys = len(conv_keys)
    fmt_string = ('\rconverting cell {{:{}d}}/{} (cell {{}})'
                  .format(len(str(n_conv_keys)), n_conv_keys))
    for i, (key, val) in enumerate(conv_keys):
        print(fmt_string.format(i+1, key), end='', flush=True)
        root = val.geometry
        treeMaster = root
        tup = conv.postOrderTraversalFlag(treeMaster)
        replace = conv.postOrderTraversalReplace(tup)
        opt_tree = conv.postOrderTraversalOptimisation(replace)
        if opt_tree is None:
            # the cell is empty, do not emit a converted cell
            continue
        j = conv.postOrderTraversalConversion(opt_tree, val.idorigin)
        objT4.volumeT4[j].fictive = False
        if j == key:
            continue
        objT4.set_key(j, key)
        objT4[key] = objT4[j]
        del objT4[j]
    print('... done', flush=True)

    return dic_cellT4, mcnp_dict


def remove_empty_cells(dic_volume):
    '''Remove cells that are patently empty.'''
    removed = set()
    to_remove = [key for key, val in dic_volume.items()
                 if val.empty() and (val.ops is None or val.ops[0] != 'UNION')]

    while to_remove:
        for key in to_remove:
            del dic_volume[key]
        removed |= set(to_remove)

        to_remove = []
        for key, val in dic_volume.items():
            if val.ops is None:
                continue
            if val.ops[0] == 'INTE' and any(x in removed for x in val.ops[1]):
                to_remove.append(key)
            elif val.ops[0] == 'UNION':
                new_args = tuple(cell for cell in val.ops[1]
                                 if cell not in removed)
                if new_args:
                    val.ops = (val.ops[0], new_args)
                else:
                    val.ops = None


def extract_used_surfaces(volumes):
    '''Return the IDs of the surfaces used in the given volumes, as a set.'''
    return set(surf for volume in volumes for surf in volume.surface_ids())

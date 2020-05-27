# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''

from ..FileHandlers.Parser.ParseMCNPCell import ParseMCNPCell
from ..Surface.SurfaceT4 import SurfaceT4
from ..Surface.ESurfaceTypeT4 import ESurfaceTypeT4 as T4S
from .DictVolumeT4 import DictVolumeT4
from .CellConversion import CellConversion
from .CellConversionError import CellConversionError
from .ByUniverse import by_universe


def construct_volume_t4(mcnp_parser, lattice_params, cell_cache_path,
                        dic_surface_t4, dic_surface_mcnp):
    '''A function that orchestrates the conversion steps for TRIPOLI-4
    volumes.'''
    dic_vol_t4 = DictVolumeT4()
    mcnp_dict, skipped_cells = ParseMCNPCell(mcnp_parser, cell_cache_path,
                                             lattice_params).parse()

    free_key = max(int(k) for k in mcnp_dict) + 1
    free_surf_key = max(max(int(k) for k in dic_surface_mcnp) + 1,
                        max(int(k) for k in dic_surface_t4) + 1)
    conv = CellConversion(free_key, free_surf_key, dic_vol_t4,
                          dic_surface_t4, dic_surface_mcnp, mcnp_dict)

    # treat TRCL
    trcl_keys = [key for key, value in mcnp_dict.items()
                 if value.trcl is not None]
    if trcl_keys:
        n_trcl_keys = len(trcl_keys)
        fmt_string = ('\rapplying TRCL transformation to cell {{:{0}d}} '
                      '({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                      .format(len(str(max(trcl_keys))),
                              len(str(n_trcl_keys))))
        for i, key in enumerate(trcl_keys):
            percent = int(100.0*i/(n_trcl_keys-1)) if n_trcl_keys > 1 else 100
            print(fmt_string.format(key, i+1, n_trcl_keys, percent),
                  end='', flush=True)
            cell = mcnp_dict[key]
            cell.geometry = conv.apply_trcl(cell.trcl, cell.geometry)
            mcnp_dict[key] = cell
        print('... done', flush=True)

    # treat complements
    n_compl = len(mcnp_dict)
    fmt_string = ('\rconverting complement for cell {{:{0}d}} '
                  '({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                  .format(len(str(max(mcnp_dict))), len(str(n_compl))))
    for i, key in enumerate(mcnp_dict):
        percent = int(100.0*i/(n_compl-1)) if n_compl > 1 else 100
        print(fmt_string.format(key, i+1, n_compl, percent),
              end='', flush=True)
        new_geom = conv.pot_complement(mcnp_dict[key].geometry)
        mcnp_dict[key].geometry = new_geom
    print('... done', flush=True)

    # treat LAT
    lat_cells = [key for key, value in mcnp_dict.items() if value.lattice]
    if lat_cells:
        n_lat_cells = len(lat_cells)
        fmt_string = ('\rdeveloping lattice in cell {{:{0}d}} '
                      '({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                      .format(len(str(max(lat_cells))),
                              len(str(n_lat_cells))))
        for i, key in enumerate(lat_cells):
            percent = int(100.0*i/(n_lat_cells-1)) if n_lat_cells > 1 else 100
            print(fmt_string.format(key, i+1, n_lat_cells, percent),
                  end='', flush=True)
            conv.develop_lattice(key)
        print('... done', flush=True)

    # update volume and surface free keys
    conv.new_cell_key = max(int(k) for k in mcnp_dict) + 1
    conv.new_surf_key = max(max(int(k) for k in dic_surface_mcnp) + 1,
                            max(int(k) for k in dic_surface_t4) + 1)

    # treat FILL
    dict_universe = by_universe(mcnp_dict)
    fill_keys = [key for key, value in mcnp_dict.items()
                 if value.fillid is not None]
    if fill_keys:
        n_fill_keys = len(fill_keys)
        fmt_string = ('\rdeveloping fill in cell {{:{0}d}} '
                      '({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                      .format(len(str(max(fill_keys))),
                              len(str(n_fill_keys))))
        for i, key in enumerate(fill_keys):
            percent = int(100.0*i/(n_fill_keys-1)) if n_fill_keys > 1 else 100
            print(fmt_string.format(key, i+1, n_fill_keys, percent),
                  end='', flush=True)
            conv.pot_fill(key, dict_universe)
        print('... done', flush=True)

    # update volume and surface free keys
    conv.new_cell_key = max(int(k) for k in mcnp_dict) + 1
    conv.new_surf_key = max(max(int(k) for k in dic_surface_mcnp) + 1,
                            max(int(k) for k in dic_surface_t4) + 1)

    conv_keys = [(key, value) for key, value in mcnp_dict.items()
                 if value.importance != 0 and value.universe == 0
                 and value.fillid is None]
    n_conv_keys = len(conv_keys)
    fmt_string = ('\rconverting cell {{:{0}d}} ({{:{1}d}}/{{:{1}d}}, {{:3d}}%)'
                  .format(len(str(max(key for key, _ in conv_keys))),
                          len(str(n_conv_keys))))

    t4_surf_numbering, matching = dic_surface_t4.number_items()
    # insert union planes into the T4 surface dictionary
    free_surf_id = max(int(k) for k in t4_surf_numbering) + 1
    union_ids = free_surf_id + 1, free_surf_id + 2
    t4_surf_numbering[union_ids[0]] = SurfaceT4(T4S.PLANEX,
                                                [1],
                                                ['aux plane for unions'])
    t4_surf_numbering[union_ids[1]] = SurfaceT4(T4S.PLANEX,
                                                [-1],
                                                ['aux plane for unions'])

    for i, (key, val) in enumerate(conv_keys):
        percent = int(100.0*i/(n_conv_keys-1)) if n_conv_keys > 1 else 100
        print(fmt_string.format(key, i+1, n_conv_keys, percent),
              end='', flush=True)
        root = val.geometry
        tup = conv.pot_flag(root)
        try:
            replace = conv.pot_replace(tup, matching)
        except CellConversionError as err:
            raise CellConversionError('{} (while converting cell {})'
                                      .format(err, key)) from None
        opt_tree = conv.pot_optimise(replace)
        if opt_tree is None:
            # the cell is empty, do not emit a converted cell
            continue
        j = conv.pot_convert(opt_tree, val.idorigin, union_ids)
        dic_vol_t4[j].fictive = False
        if j == key:
            continue
        dic_vol_t4.replace_key(j, key)
    print('... done', flush=True)

    return dic_vol_t4, mcnp_dict, t4_surf_numbering, skipped_cells


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

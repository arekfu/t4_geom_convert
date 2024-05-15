# Copyright 2019-2024 French Alternative Energies and Atomic Energy Commission
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

from warnings import warn

from MIP.geom.main import extract_surfaces_list

from ..Progress import Progress
from ..FileHandlers.Parser.ParseMCNPCell import ParseMCNPCell
from ..Surface.SurfaceT4 import SurfaceT4
from ..Surface.ESurfaceTypeT4 import ESurfaceTypeT4 as T4S
from ..Surface.SurfaceConversionError import SurfaceConversionError
from ..Transformation.Transformation import transformation
from .DictVolumeT4 import DictVolumeT4
from .CellConversion import CellConversion
from .CellConversionError import CellConversionError
from ..Surface.ConversionSurfaceMCNPToT4 import convert_mcnp_surface
from .ByUniverse import by_universe
from .CellInlining import inline_cells


def construct_volume_t4(mcnp_parser, lattice_params, cell_cache_path,
                        dic_surface_t4, dic_surface_mcnp, inline_filled,
                        inline_filling, max_inline_score):
    '''A function that orchestrates the conversion steps for TRIPOLI-4
    volumes.'''
    dic_vol_t4 = DictVolumeT4()
    mcnp_dict, skipped_cells = ParseMCNPCell(mcnp_parser, cell_cache_path,
                                             lattice_params).parse()

    tr_surf_ids = extract_tr_surf_ids(mcnp_dict) - set(dic_surface_mcnp)
    if tr_surf_ids:
        with Progress('generating implicitly defined surface',
                      len(tr_surf_ids), max(tr_surf_ids)) as progress:
            for i, tr_surf_id in enumerate(tr_surf_ids):
                progress.update(i, tr_surf_id)
                surf_id = tr_surf_id % 1000
                cell_id = tr_surf_id // 1000
                trs = mcnp_dict[cell_id].trcl
                tr_surfs = dic_surface_mcnp[surf_id]
                for tr in trs:
                    tr_surfs = [(transformation(tr, surf), side)
                                for surf, side in tr_surfs]
                dic_surface_mcnp[tr_surf_id] = tr_surfs
                t4_tr_surfs = convert_mcnp_surface(tr_surf_id, tr_surfs)
                dic_surface_t4[tr_surf_id] = t4_tr_surfs

    free_key = max(int(k) for k in mcnp_dict) + 1
    free_surf_key = max(max(int(k) for k in dic_surface_mcnp) + 1,
                        max(int(k) for k in dic_surface_t4) + 1)
    conv = CellConversion(free_key, free_surf_key, dic_vol_t4,
                          dic_surface_t4, dic_surface_mcnp, mcnp_dict)

    # treat TRCL
    trcl_keys = [key for key, value in mcnp_dict.items()
                 if value.trcl is not None]
    if trcl_keys:
        with Progress('applying TRCL transformation to cell',
                      len(trcl_keys), max(trcl_keys)) as progress:
            for i, key in enumerate(trcl_keys):
                progress.update(i, key)
                cell = mcnp_dict[key]
                cell.geometry = conv.apply_trcl(cell.trcl, cell.geometry)
                mcnp_dict[key] = cell

    # treat complements
    with Progress('converting complement for cell',
                  len(mcnp_dict), max(mcnp_dict)) as progress:
        for i, key in enumerate(mcnp_dict):
            progress.update(i, key)
            new_geom = conv.pot_complement(mcnp_dict[key].geometry)
            mcnp_dict[key].geometry = new_geom

    # treat LAT
    lat_cells = [key for key, value in mcnp_dict.items() if value.lattice]
    if lat_cells:
        with Progress('developing lattice in cell',
                      len(lat_cells), max(lat_cells)) as progress:
            for i, key in enumerate(lat_cells):
                progress.update(i, key)
                conv.develop_lattice(key)

    # treat FILL
    dict_universe = by_universe(mcnp_dict)
    fill_keys = [key for key, value in mcnp_dict.items()
                 if value.fillid is not None and value.universe == 0]
    if fill_keys:
        with Progress('developing fill in cell',
                      len(fill_keys), max(fill_keys)) as progress:
            for i, key in enumerate(fill_keys):
                progress.update(i, key)
                try:
                    conv.pot_fill(key, dict_universe, inline_filled,
                                  inline_filling)
                except SurfaceConversionError as err:
                    raise SurfaceConversionError(f'{err} (while converting '
                                                 f'cell {key})') from None

    # consider inlining cells
    inline_cells(mcnp_dict, max_inline_score)

    conv_keys = [(key, value) for key, value in mcnp_dict.items()
                 if value.importance != 0 and value.universe == 0
                 and value.fillid is None]

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

    with Progress('converting cell', len(conv_keys),
                  max(key for key, _ in conv_keys)) as progress:
        for i, (key, val) in enumerate(conv_keys):
            progress.update(i, key)
            try:
                j = conv.pot_convert(val, matching, union_ids)
            except CellConversionError as err:
                raise CellConversionError(f'{err} (while converting cell '
                                          f'{key})') from None
            if j is None:
                # the converted cell is empty
                continue
            dic_vol_t4[key] = dic_vol_t4[j].copy()
            dic_vol_t4[key].fictive = False

    return dic_vol_t4, mcnp_dict, t4_surf_numbering, skipped_cells, union_ids


def extract_tr_surf_ids(mcnp_dict):
    '''Return the list of MCNP surface IDs above 1000.

    Surface IDs above 1000 are interpreted by MCNP as (surf_id + 1000*cell_id),
    where cell_id indicates a cell with a trcl card. The surface is modified by
    applying the trcl card of the cell.
    '''
    tr_surf_ids = []
    for value in mcnp_dict.values():
        surfs = extract_surfaces_list(value.geometry)
        tr_surf_ids.extend(abs(int(surf)) for surf in surfs if surf >= 1000)
    return set(tr_surf_ids)


def remove_empty_volumes(dic_volume, union_ids):
    '''Remove cells that are patently empty.'''
    removed = set()
    to_remove = [key for key, val in dic_volume.items() if val.empty()]

    while to_remove:
        removed_at_this_step = set()
        for key in to_remove:
            val = dic_volume[key]
            if val.ops is None or val.ops[0] != 'UNION':
                # This volume is just an intersection with an empty volume, so we can
                # remove it
                del dic_volume[key]
                removed_at_this_step.add(key)
                continue

            # Here val is patently empty, but it also contains a union with other
            # volumes, so it may not be empty after all. So we replace the surface
            # definitions with an empty volume
            val.pluses = set([union_ids[0]])
            val.minuses = set([union_ids[1]])

        removed |= removed_at_this_step

        # update the list of volumes that must be removed
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


def remove_unused_volumes(dic):
    '''Remove unused virtual (``FICTIVE``) volumes from the given dictionary.
    This function modifies the given dictionary in place.

    :param DictVolumeT4 dic: a dictionary of :class:`~.VolumeT4` objects.

    >>> from .VolumeT4 import VolumeT4
    >>> dic = DictVolumeT4()
    >>> dic[1] = VolumeT4([], [], ops=['UNION', (2, 3)], fictive=False)
    >>> dic[2] = VolumeT4([], [], ops=None, fictive=True)
    >>> dic[3] = VolumeT4([], [], ops=None, fictive=True)
    >>> dic[4] = VolumeT4([], [], ops=None, fictive=True)
    >>> dic[5] = VolumeT4([], [], ops=None, fictive=False)
    >>> remove_unused_volumes(dic)
    >>> sorted(list(dic.keys()))
    [1, 2, 3, 5]
    '''
    fictives = set(key for key, volume in dic.items() if volume.fictive)
    used = set(key for volume in dic.values() if volume.ops is not None
               for args in volume.ops[1:] for key in args)
    unused = fictives - used
    for key in unused:
        del dic[key]

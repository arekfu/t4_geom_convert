# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from .ConversionSurfaceMCNPToT4 import conversionSurfaceMCNPToT4
from .SurfaceT4 import SurfaceT4
from .SurfaceCollection import SurfaceCollection
from .ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from collections import OrderedDict


def constructSurfaceT4(mcnpParser):
    '''
    :brief: method constructing a dictionary with the id
    of the surface as a key and the instance of SurfaceT4 as a value
    '''
    dic_surface_t4_new = OrderedDict()
    dic_surface_t4, dic_surfaceMCNP = conversionSurfaceMCNPToT4(mcnpParser)
    free_id = max(int(k) for k in dic_surface_t4.keys()) + 1
    n_surfaces = len(dic_surface_t4)
    fmt_string = ('\rconverting surface {{:{}d}} ({{:3d}}%)'
                  .format(len(str(max(dic_surface_t4)))))
    for i, (key, surf_coll) in enumerate(dic_surface_t4.items()):
        percent = int(100.0*i/(n_surfaces-1)) if n_surfaces > 1 else 100
        print(fmt_string.format(key, percent), end='', flush=True)
        aux_ids = []
        for surf, side in surf_coll.surfs[1:]:
            dic_surface_t4_new[free_id] = (surf, [])
            aux_ids.append(side * free_id)
            free_id += 1
        dic_surface_t4_new[key] = (surf_coll.surfs[0][0], aux_ids)

    union_ids = free_id + 1, free_id + 2
    dic_surface_t4_new[union_ids[0]] = (SurfaceT4(T4S.PLANEX, [1], ['aux plane for unions']), [])
    dic_surface_t4_new[union_ids[1]] = (SurfaceT4(T4S.PLANEX, [-1], ['aux plane for unions']), [])
    print('... done', flush=True)

    return dic_surface_t4_new, dic_surfaceMCNP, union_ids

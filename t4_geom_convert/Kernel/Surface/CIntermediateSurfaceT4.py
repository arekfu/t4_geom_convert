# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateSurfaceT4.py


.. doctest:: CIntermediateSurfaceT4
    :hide:
    >>> from CIntermediateSurfaceT4 import CIntermediateSurfaceT4
    >>> dic_SurfaceT4 = CIntermediateSurfaceT4().m_constructSurfaceT4()
    >>> for key in p.keys():
    >>>     print('type Surface', dic_SurfaceT4[key].typeSurface)
    >>>     print('param Surface', dic_SurfaceT4[key].paramSurface)

'''
from ..Surface.CSurfaceConversionMCNPToT4 import CSurfaceConversionMCNPToT4
from ..Surface.CSurfaceT4 import CSurfaceT4
from ..Surface.ESurfaceTypeT4 import ESurfaceTypeT4Eng as T4S
from ..Transformation.CConversionSurfaceTransformed import CConversionSurfaceTransformed
from collections import OrderedDict

class CIntermediateSurfaceT4(object):
    '''
    :brief: Class which associate the T4 surface with the Class CSURFACET4
    '''

    def m_constructSurfaceT4(self):
        '''
        :brief: method constructing a dictionary with the id
        of the surface as a key and the instance of CSurfaceT4 as a value
        '''
        dic_newSurfaceT4 = OrderedDict()
        dic_surfaceT4, dic_surfaceMCNP = CSurfaceConversionMCNPToT4().m_conversionMCNPToT4()
        #print('surfaceT4')
        dic_surfaceT4Tr, dic_surfaceMCNPTr = CConversionSurfaceTransformed().m_conversionSurfaceTransformed()
        #print('surfaceT4Tr')
        dic_surfaceT4.update(dic_surfaceT4Tr)
        dic_surfaceMCNP.update(dic_surfaceMCNPTr)
        #print(dic_surfaceT4Tr)
        #print(dic_surfaceT4)
        free_id = max(int(k) for k in dic_surfaceT4.keys()) + 1
        keyS = 100000
        for key, surf_coll in dic_surfaceT4.items():
#             print('surface', key)
            fixed_surfs = surf_coll.fixed
            fixed_ids = []
            for surf, side in fixed_surfs:
                dic_newSurfaceT4[free_id] = (surf, [])
                fixed_ids.append(side * free_id)
                free_id += 1
            dic_newSurfaceT4[key] = (surf_coll.main, fixed_ids)
        dic_newSurfaceT4[keyS + 1] = (CSurfaceT4(T4S.PLANEX, [1], ['aux plane for unions']), [])
        dic_newSurfaceT4[keyS + 2] = (CSurfaceT4(T4S.PLANEX, [-1], ['aux plane for unions']), [])
        return dic_newSurfaceT4, dic_surfaceMCNP

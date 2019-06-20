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
from ..Transformation.CConversionSurfaceTransformed import CConversionSurfaceTransformed

class CIntermediateSurfaceT4(object):
    '''
    :brief: Class which associate the T4 surface with the Class CSURFACET4
    '''

    def __init__(self):
        '''
        Constructor
        '''
        

    def m_constructSurfaceT4(self):
        '''
        :brief: method constructing a dictionary with the id
        of the surface as a key and the instance of CSurfaceT4 as a value
        '''
        dic_newSurfaceT4 = dict()
        dic_surfaceT4 = CSurfaceConversionMCNPToT4().m_conversionMCNPToT4()
        print('surfaceT4')
        dic_surfaceT4Tr = CConversionSurfaceTransformed().m_conversionSurfaceTransformed()
        print('surfaceT4Tr')
        dic_surfaceT4.update(dic_surfaceT4Tr)
        print(dic_surfaceT4Tr)
        print(dic_surfaceT4)
        free_id = max(int(k) for k in dic_surfaceT4.keys()) + 1
        keyS = 100000
        for key, surfs in dic_surfaceT4.items():
            print('surface', key)
            extra_surfs = surfs[1:]
            extra_ids = []
            for (p_typeSurface, p_listCoefSurface), side in extra_surfs:
                dic_newSurfaceT4[free_id] = (CSurfaceT4(p_typeSurface.name, p_listCoefSurface), [])
                extra_ids.append(side * free_id)
                free_id += 1
            p_typeSurface, p_listCoefSurface = surfs[0]
            dic_newSurfaceT4[key] = (CSurfaceT4(p_typeSurface.name, p_listCoefSurface), extra_ids)
        dic_newSurfaceT4[keyS + 1] = (CSurfaceT4('PLANEX', [1]), [])
        dic_newSurfaceT4[keyS + 2] = (CSurfaceT4('PLANEX', [-1]), [])
        return dic_newSurfaceT4

# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateSurfaceT4.py
'''
from Surface.CSurfaceConversionMCNPToT4 import CSurfaceConversionMCNPToT4
from Surface.CSurfaceT4 import CSurfaceT4

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
        :brief: method constructing a dictionary with the id of the surface as a key and the instance of CSurfaceT4 as a value
        '''
        dic_newSurfaceT4 = dict()
        dic_surfaceT4 = CSurfaceConversionMCNPToT4().m_conversionMCNPToT4()
        for key,val in dic_surfaceT4.items() :  
            p_typeSurface, p_listCoefSurface = val 
            dic_newSurfaceT4[key] = CSurfaceT4(p_typeSurface.name,p_listCoefSurface)
        return dic_newSurfaceT4
    
# p = CIntermediateSurfaceT4().m_constructSurfaceT4()
# print(p[1].typeSurface, p[10].paramSurface)
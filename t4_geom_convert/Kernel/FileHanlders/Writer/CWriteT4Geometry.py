# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4Geometry.py
'''
from ...Surface.CIntermediateSurfaceT4 import CIntermediateSurfaceT4
from ...Volume.CIntermediateVolumeT4 import CIntermediateVolumeT4

class CWriteT4Geometry(object):
    '''
    :brief: Class which write the geometry part of the T4 input file
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def m_writeT4Geometry(self, f):
        '''
        :brief: method separated in two part,
        the first for the surface and the second for the volume
        This method fills a file of the geometry for the input file of T4
        '''
        f.write("GEOMETRY \n")
        f.write("\n")
        f.write("TITLE title")
        f.write("\n")
        dic_surface = CIntermediateSurfaceT4().m_constructSurfaceT4()
        for key, (surf, _extra_ids) in dic_surface.items():
            list_paramSurface = surf.paramSurface
            print(key, surf.typeSurface, list_paramSurface)
            s_paramSurface = ' '.join(str(element) for element in list_paramSurface)
            f.write("SURFACE %s %s %s\n" % (key, surf.typeSurface,
                                            s_paramSurface))
        f.write("\n")
        dic_volume = CIntermediateVolumeT4(dic_surface).m_constructVolumeT4()
        for k in dic_volume.keys():
            s_operator = dic_volume[k].operator
            s_param = dic_volume[k].param
            s_fictive = dic_volume[k].fictive
            f.write("VOLU %s %s %s %s ENDV  \n" % (k, s_operator, s_param, s_fictive))
        f.write("\n")
        f.write("ENDG")
        f.write("\n")

# CWriteT4Geometry().m_writeT4Geometry()

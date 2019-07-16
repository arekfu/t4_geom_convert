# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4Geometry.py
'''
from ...Surface.CIntermediateSurfaceT4 import CIntermediateSurfaceT4
from ...Volume.CIntermediateVolumeT4 import CIntermediateVolumeT4
import pickle
from ...Configuration.CConfigParameters import CConfigParameters

class CWriteT4Geometry(object):
    '''
    :brief: Class which write the geometry part of the T4 input file
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def writeT4Geometry(self, f):
        '''
        :brief: method separated in two part,
        the first for the surface and the second for the volume
        This method fills a file of the geometry for the input file of T4
        '''
        f.write("GEOMETRY\n\nTITLE title\n\nHASH_TABLE\n\n")
        input_file = CConfigParameters().readNameMCNPInputFile()
        dicCell_name = input_file + '_dicCell'
        dicSurface_name = input_file + '_dicSurface'
        try:
            with open(dicSurface_name, mode='rb') as dicfile:
                dic_surfaceT4, dic_surfaceMCNP  = pickle.load(dicfile)
                print('_dicSurface lu')
        except:
            dic_surfaceT4, dic_surfaceMCNP = CIntermediateSurfaceT4().constructSurfaceT4()
            with open(dicSurface_name, mode='wb') as dicfile:
                pickle.dump((dic_surfaceT4, dic_surfaceMCNP), dicfile)
        try:
            with open(dicCell_name, mode='rb') as dicfile:
                dic_volume,surf_used, mcnp_new_dict, dic_surfaceT4 = pickle.load(dicfile)
                print('_dicCell lu')
        except:
            dic_volume, surf_used, mcnp_new_dict = CIntermediateVolumeT4(dic_surfaceT4, dic_surfaceMCNP).constructVolumeT4()
            with open(dicCell_name, mode='wb') as dicfile:
                pickle.dump((dic_volume, surf_used, mcnp_new_dict, dic_surfaceT4), dicfile)
        for key in sorted(surf_used):
            surf, _ = dic_surfaceT4[key]
            list_paramSurface = surf.paramSurface
            s_paramSurface = ' '.join(str(element) for element in list_paramSurface)
            s_comment = '' if not surf.idorigin else '// ' + str(surf.idorigin)
            f.write("SURF %s %s %s %s\n" % (key, surf.typeSurface.name,
                                            s_paramSurface, s_comment))
        f.write("\n")

        for k, val in dic_volume.items():
            s_params = ' '.join(str(param) for param in val.params)
            s_fictive = val.fictive
            if val.idorigin:
                s_comment = "// %s" %val.idorigin
            else:
                s_comment = ""
            f.write("VOLU %s %s %s ENDV %s\n" % (k, s_params, s_fictive, s_comment))
        f.write("\n")
        f.write("ENDG")
        f.write("\n")
        return dic_volume, mcnp_new_dict

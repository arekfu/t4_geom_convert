# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4GeomComp.py
'''
from ...GeomComp.CIntermediateGeomCompT4 import CIntermediateGeomCompT4


class CWriteT4GeomComp(object):
    '''
    :brief: Class which write the geometry part of the T4 input file
    '''

    def __init__(self, p_dicVol, mcnp_new_dict):
        '''
        Constructor
        '''
        self.dicVol = p_dicVol
        self.mcnp_new_dict = mcnp_new_dict
    def writeT4GeomComp(self, f):
        '''
        :brief: method writing GeomComp of the T4 input file
        '''
        f.write("\nGEOMCOMP\n")
        dic_geomComp = CIntermediateGeomCompT4().constructGeomCompT4(self.dicVol, self.mcnp_new_dict)
        for k in dic_geomComp.keys():
            p_materialName = str(k)
            p_numberOfCell = str(dic_geomComp[k].volumeNumberMaterial)
            p_listVolumeId = dic_geomComp[k].listVolumeId
            f.write("%s %s %s\n" % ("m" + p_materialName, p_numberOfCell,
                                    p_listVolumeId))
        f.write("END_GEOMCOMP")
        f.write("\n")

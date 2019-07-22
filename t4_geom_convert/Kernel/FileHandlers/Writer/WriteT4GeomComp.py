# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
from ...GeomComp.ConstructGeomCompT4 import constructGeomCompT4


def writeT4GeomComp(dic_vol, mcnp_new_dict, ofile):
    '''
    :brief: method writing GeomComp of the T4 input file
    '''
    ofile.write("\nGEOMCOMP\n")
    dic_geomComp = constructGeomCompT4(dic_vol, mcnp_new_dict)
    for k in dic_geomComp.keys():
        p_materialName = str(k)
        p_numberOfCell = str(dic_geomComp[k].volumeNumberMaterial)
        p_listVolumeId = dic_geomComp[k].listVolumeId
        ofile.write("%s %s %s\n" % ("m" + p_materialName, p_numberOfCell,
                                    p_listVolumeId))
    ofile.write("END_GEOMCOMP")
    ofile.write("\n")

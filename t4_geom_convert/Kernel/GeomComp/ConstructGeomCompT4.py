# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateGeomCompT4.py
'''

from .CDictGeomCompT4 import CDictGeomCompT4
from .CGeomCompT4 import CGeomCompT4
from collections import defaultdict, OrderedDict

def constructGeomCompT4(dicVol, dic_cellMCNP):
    '''
    :brief: method constructing a dictionary with the id of the
    material as a key and the instance of CGeomCompT4 as a value
    '''
    dic_geomCompT4 = OrderedDict()
    dic_partialGeomComp = OrderedDict()
    obj_T4 = CDictGeomCompT4(dic_geomCompT4)
    for key, val in dicVol.items():
        if val.fictive:
            continue
        if val.idorigin:
            volID = val.idorigin[0][0]
        else:
            volID = key
        density = dic_cellMCNP[volID].density
        if density is None:
            materialName = dic_cellMCNP[volID].materialID
        else:
            materialName = dic_cellMCNP[volID].materialID + '_' + density
        if materialName not in dic_partialGeomComp:
            dic_partialGeomComp[materialName] = []
        dic_partialGeomComp[materialName].append(key)
    for key in dic_partialGeomComp.keys():
        numberOfCell = len(dic_partialGeomComp[key])
        listCell = dic_partialGeomComp[key]
        obj_T4[key] = CGeomCompT4(numberOfCell, " ".join(str(x) for x in listCell))
    return obj_T4.geomCompT4

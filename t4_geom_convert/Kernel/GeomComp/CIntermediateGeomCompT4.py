# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateGeomCompT4.py
'''

from ..GeomComp.CDictGeomCompT4 import CDictGeomCompT4
from ..Volume.CDictCellMCNP import CDictCellMCNP
from ..GeomComp.CGeomCompT4 import CGeomCompT4
from collections import defaultdict, OrderedDict

class CIntermediateGeomCompT4(object):
    '''
    :brief: Class which associate the T4 surface with the Class CSURFACET4
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def m_constructGeomCompT4(self, dicVol, dic_cellMCNP):
        '''
        :brief: method constructing a dictionary with the id of the
        material as a key and the instance of CGeomCompT4 as a value
        '''
        dic_geomCompT4 = OrderedDict()
        dic_partialGeomComp = OrderedDict()
        obj_T4 = CDictGeomCompT4(dic_geomCompT4)
        for key, val in dicVol.items():
            if val.fictive != '':
                continue
            if val.idorigin:
                volID = val.idorigin[0][0]
            else:
                volID = key
            materialName = dic_cellMCNP[volID].materialID
            if materialName not in dic_partialGeomComp:
                dic_partialGeomComp[materialName] = []
            dic_partialGeomComp[materialName].append(key)
        for key in dic_partialGeomComp.keys():
            numberOfCell = len(dic_partialGeomComp[key])
            listCell = dic_partialGeomComp[key]
            obj_T4[key] = CGeomCompT4(numberOfCell, " ".join(str(x) for x in listCell))
        return obj_T4.geomCompT4

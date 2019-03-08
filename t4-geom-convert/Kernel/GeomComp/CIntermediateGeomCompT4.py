# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateGeomCompT4.py
'''

from GeomComp.CDictGeomCompT4 import CDictGeomCompT4
from Volume.CIntermediateVolumeT4 import CIntermediateVolumeT4
from Composition.CIntermediateCompositionT4 import CIntermediateCompositionT4
from Volume.CDictCellMCNP import CDictCellMCNP
from GeomComp.CGeomCompT4 import CGeomCompT4

class CIntermediateGeomCompT4(object):
    '''
    :brief: Class which associate the T4 surface with the Class CSURFACET4
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def m_constructGeomCompT4(self):
        '''
        :brief: method constructing a dictionary with the id of the material as a key and the instance of CGeomCompT4 as a value
        '''
        dic_geomCompT4 = dict()
        dic_partialGeomComp = dict()
        obj_T4 = CDictGeomCompT4(dic_geomCompT4)
        dic_cellMCNP = CDictCellMCNP().d_cellMCNP
        #dic_compositionT4 = CIntermediateCompositionT4().m_constructCompositionT4()
        for key in dic_cellMCNP.keys() :
            obj_cellMCNP = dic_cellMCNP[key]
            materialName = obj_cellMCNP.materialID
            dic_partialGeomComp[materialName] = ""
        
        for key in dic_cellMCNP.keys() : 
            cellID = str(key)
            obj_cellMCNP = dic_cellMCNP[key]
            materialName = obj_cellMCNP.materialID 
            dic_partialGeomComp[materialName] = dic_partialGeomComp[materialName] + " " + cellID
        for key in dic_partialGeomComp.keys():
            numberOfCell = len(dic_partialGeomComp[key].split(" ")) - 1
            listCell = dic_partialGeomComp[key]
            obj_T4.__setitem__(key, CGeomCompT4(numberOfCell,listCell))
        return obj_T4.geomCompT4
  
    
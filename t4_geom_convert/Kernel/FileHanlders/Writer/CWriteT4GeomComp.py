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

    def __init__(self):
        '''
        Constructor
        '''
    def m_writeT4GeomComp(self):
        '''
        :brief: method writing GeomComp of the T4 input file
        '''
        f = open('testconnverti.txt', "a+")
        f.write("\n GEOMCOMP \n")
        f.write("\n")
        dic_geomComp = CIntermediateGeomCompT4().m_constructGeomCompT4()
        for k in dic_geomComp.keys():
            p_materialName = str(k)
            p_numberOfCell = str(dic_geomComp[k].volumeNumberMaterial)
            p_listVolumeId = dic_geomComp[k].listVolumeId
            f.write("%s %s %s \n" % ("m" + p_materialName, p_numberOfCell,\
                                     p_listVolumeId))
        f.write("\n")
        f.write("END_GEOMCOMP")
        f.write("\n")
        f.close()

CWriteT4GeomComp().m_writeT4GeomComp()

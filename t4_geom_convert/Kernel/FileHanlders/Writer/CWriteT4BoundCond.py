# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4BoundCond.py
'''
from ...BoundaryCondition.CConversionBoundaryCondition import CConversionBoundaryCondition

class CWriteT4BoundCond(object):
    '''
    :brief: Class which write the geometry part of the T4 input file
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def m_writeT4BoundCond(self):
        '''
        :brief: method writing GeomComp of the T4 input file
        '''
        f = open('testconnverti.txt', "a+")
        f.write("\r\n BOUNDARY_CONDITION \r\n")
        f.write("\r\n")
        d_boundCond = CConversionBoundaryCondition().m_conversionBoundCond()
        for k in d_boundCond.keys():
            p_materialName = str(k)
            l_surfaceID = d_boundCond[k].surfaceID
            l_typeOfBound = d_boundCond[k].typeOfBound
            for i in range(0,len(l_surfaceID)):
                f.write("%s %s %s \r" % (p_materialName, l_surfaceID[i], l_typeOfBound[i]))
        f.write("\r\n")
        f.write("END_BOUNDARY_CONDITION")
        f.close()
CWriteT4BoundCond().m_writeT4BoundCond()

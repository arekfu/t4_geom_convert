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
        f.write("\r\n ALL_COMPLETE \r\n")
        f.write("\r\n")
        d_boundCond = CConversionBoundaryCondition().m_conversionBoundCond()
        f.write(str(len(d_boundCond)))
        f.write("\r\n")
        for k in d_boundCond.keys():
            p_typeOfBound = d_boundCond[k].typeOfBound
            f.write("%s %s \r" %(str(k), p_typeOfBound))
        f.write("\r\n")
        f.write("END_BOUNDARY_CONDITION")
        f.write("\r\n")
        f.close()
CWriteT4BoundCond().m_writeT4BoundCond()

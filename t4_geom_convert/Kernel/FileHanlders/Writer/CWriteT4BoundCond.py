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
    def m_writeT4BoundCond(self, f):
        '''
        :brief: method writing GeomComp of the T4 input file
        '''
        f.write("\n BOUNDARY_CONDITION \n")
        f.write("\n")
        f.write("\n ALL_COMPLETE \n")
        f.write("\n")
        d_boundCond = CConversionBoundaryCondition().m_conversionBoundCond()
        f.write(str(len(d_boundCond)))
        f.write("\n")
        for k in d_boundCond.keys():
            p_typeOfBound = d_boundCond[k].typeOfBound
            f.write("%s %s \n" %(str(k), p_typeOfBound))
        f.write("\n")
        f.write("END_BOUNDARY_CONDITION")
        f.write("\n")
# CWriteT4BoundCond().m_writeT4BoundCond()

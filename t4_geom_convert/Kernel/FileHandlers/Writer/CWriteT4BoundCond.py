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
    def writeT4BoundCond(self, f):
        '''
        :brief: method writing GeomComp of the T4 input file
        '''
        d_boundCond = CConversionBoundaryCondition().conversionBoundCond()
        if not d_boundCond:
            return
        f.write("\nBOUNDARY_CONDITION\n")
        f.write(str(len(d_boundCond)))
        f.write("\n")
        for k in d_boundCond.keys():
            p_typeOfBound = d_boundCond[k].typeOfBound
            f.write("ALL_COMPLETE %s %s\n" %(p_typeOfBound, k))
        f.write("END_BOUNDARY_CONDITION")
        f.write("\n")
# CWriteT4BoundCond().writeT4BoundCond()

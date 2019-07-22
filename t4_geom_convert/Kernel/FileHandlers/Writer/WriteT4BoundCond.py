# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CWriteT4BoundCond.py
'''
from ...BoundaryCondition.CConversionBoundaryCondition import CConversionBoundaryCondition


def writeT4BoundCond(dic_surf_mcnp, ofile):
    '''
    :brief: method writing GeomComp of the T4 input file
    '''
    d_boundCond = CConversionBoundaryCondition(dic_surf_mcnp).conversionBoundCond()
    if not d_boundCond:
        return
    ofile.write("\nBOUNDARY_CONDITION\n")
    ofile.write(str(len(d_boundCond)))
    ofile.write("\n")
    for k in d_boundCond.keys():
        p_typeOfBound = d_boundCond[k].typeOfBound
        ofile.write("ALL_COMPLETE %s %s\n" %(p_typeOfBound, k))
    ofile.write("END_BOUNDARY_CONDITION")
    ofile.write("\n")

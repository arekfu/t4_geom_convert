# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateBoundaryCondition.py
'''
import re
from ...MIP import mip
from ...MIP.geom.cells import get_cells
from ..FileHanlders.Parser.CParseMCNPSurface import CParseMCNPSurface
from ..FileHanlders.Parser.CParseMCNPCell import CParseMCNPCell
from ..BoundaryCondition.CBoundCond import CBoundCond


class CConversionBoundaryCondition(object):
    '''
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def m_recuperateBoundaryCondition(self):
        '''
        :brief: method constructing a dictionary with the id of the
        material as a key and the instance of CBoundCondT4 as a value
        '''
        d_boundCond = dict()
        d_surface = CParseMCNPSurface().m_parsingSurface()
        inputCell = mip.MIP(CParseMCNPCell().inputMCNP)
        cellParser = get_cells(inputCell, lim=None)
        for k, v in list(cellParser.items()):
            l_geometry = []
            l_surfaceID = []
            l_typeOfBC = []
            geometry = v[1]
            l_geometry = [abs(int(number)) for number in re.findall(r'-?\d+\.?\d*',\
                                                                    geometry)]
            for element in l_geometry:
                if d_surface[element] and str(d_surface[element].boundaryCond) != '':
                    l_surfaceID.append(element)
                    l_typeOfBC.append(d_surface[element].boundaryCond)
            if l_surfaceID != [] and l_typeOfBC != []:
                d_boundCond[k] = CBoundCond(l_surfaceID,l_typeOfBC)
        return d_boundCond

    def m_conversionBoundCond(self):
        '''
        '''
        d_boundCondT4 = dict()
        d_boundcondMCNP = self.m_recuperateBoundaryCondition()
        for k in d_boundcondMCNP.keys():
            l_boundCondT4 = []
            l_surfaceID = d_boundcondMCNP[k].surfaceID
            l_boundCondMCNP = d_boundcondMCNP[k].typeOfBound
            for element in l_boundCondMCNP:
                if element == '*':
                    l_boundCondT4.append('REFLECTION')
                if element == '+':
                    l_boundCondT4.append('COSINUS')
            d_boundCondT4[k] = CBoundCond(l_surfaceID, l_boundCondT4)
        return d_boundCondT4

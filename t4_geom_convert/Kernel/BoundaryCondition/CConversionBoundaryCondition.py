# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateBoundaryCondition.py
'''
from .CBoundCond import CBoundCond
from collections import OrderedDict


class CConversionBoundaryCondition(object):
    '''
    '''


    def __init__(self, dic_surf_mcnp):
        '''
        Constructor
        '''
        self.dic_surf_mcnp = dic_surf_mcnp

    def recuperateBoundaryCondition(self):
        '''
        :brief: method constructing a dictionary with the id of the
        material as a key and the instance of CBoundCondT4 as a value
        '''
        d_boundCond = OrderedDict()
        for k, v in list(self.dic_surf_mcnp.items()):
            if v.boundaryCond != '':
                p_typeOfBC = v.boundaryCond
                d_boundCond[k] = CBoundCond(p_typeOfBC)
        return d_boundCond

    def conversionBoundCond(self):
        '''
        '''
        d_boundCondT4 = OrderedDict()
        d_boundcondMCNP = self.recuperateBoundaryCondition()
        for k in d_boundcondMCNP.keys():
            p_boundCondMCNP = d_boundcondMCNP[k].typeOfBound
            if p_boundCondMCNP == '*':
                p_typeOfBC = 'REFLECTION'
            if p_boundCondMCNP == '+':
                p_typeOfBC = 'COSINUS'
            d_boundCondT4[k] = CBoundCond(p_typeOfBC)
        return d_boundCondT4

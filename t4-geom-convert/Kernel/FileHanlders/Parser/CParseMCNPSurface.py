# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CParseMCNPSurface.py
'''
import mip
from geom.surfaces import get_surfaces

from FileHanlders.Parser.Parameters import f_inputMCNP
from Surface.CSurfaceMCNP import CSurfaceMCNP
from Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP

class CParseMCNPSurface(object):
    '''
    :brief: Class which parse the block Surface
    '''


    def __init__(self):
        '''
        Constructor
        :param: f_inputMCNP : input file of MCNP
        '''
        self.inputMCNP = f_inputMCNP
        
    def m_parsingSurface(self):
        
        '''
        :brief method which permit to recover the information of each line of the block SURFACE
        :return: dictionary which contains the ID of the surfaces as a key and as a value, a object from the class CSurfaceMCNP
        '''
        inputCell = mip.MIP(self.inputMCNP)
        surfaceParser = get_surfaces(inputCell, lim=None)
        dictSurface = dict()
        for k,v in list(surfaceParser.items()):
            p_1, p_2, p_typeSurface, l_paramSurface = v
            enumSurface = getattr(ESurfaceTypeMCNP,p_typeSurface.upper())
            dictSurface[k] = CSurfaceMCNP(p_1, p_2, enumSurface, l_paramSurface)
        return dictSurface
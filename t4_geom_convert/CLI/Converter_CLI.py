# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : Converter_CLI..py
'''
from t4_geom_convert.Kernel.FileHanlders.Writer.CWriteT4Geometry import CWriteT4Geometry
from t4_geom_convert.Kernel.FileHanlders.Writer.CWriteT4Composition import CWriteT4Composition
from t4_geom_convert.Kernel.FileHanlders.Writer.CWriteT4GeomComp import CWriteT4GeomComp
"""
Usage:
        Converter_CLI.py conversion <p_nameT4File> <p_nameMCNPFile>
"""

from docopt_dispatch import dispatch

@dispatch.on('conversion')
def conversion(p_nameT4File, p_nameMCNPFile, **kwargs):
    
    
    CWriteT4Geometry().m_writeT4Geometry()
    CWriteT4Composition().m_writeT4Composition()
    CWriteT4GeomComp().m_writeT4GeomComp()

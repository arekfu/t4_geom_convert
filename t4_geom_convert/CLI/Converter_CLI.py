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
from t4_geom_convert.Kernel.Configuration.CConfigParameters import CConfigParameters
"""
Usage:
        Converter_CLI.py conversion <p_nameT4File> <p_nameMCNPFile>
"""

def conversion(p_nameT4File, p_nameMCNPFile):
    with open(p_nameT4File, 'w') as ofile:
        CWriteT4Geometry().m_writeT4Geometry(ofile)
        CWriteT4Composition().m_writeT4Composition(ofile)
        CWriteT4GeomComp().m_writeT4GeomComp(ofile)

if __name__ == '__main__':
    config = CConfigParameters()
    t4_fname = config.m_readNameT4InputFile()
    mcnp_fname = config.m_readNameMCNPInputFile()
    conversion(t4_fname, mcnp_fname)

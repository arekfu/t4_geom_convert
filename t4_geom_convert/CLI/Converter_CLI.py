# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : Converter_CLI..py
'''
from ..Kernel.FileHanlders.Writer.CWriteT4Geometry import CWriteT4Geometry
from ..Kernel.FileHanlders.Writer.CWriteT4Composition import CWriteT4Composition
from ..Kernel.FileHanlders.Writer.CWriteT4GeomComp import CWriteT4GeomComp
from ..Kernel.Configuration.CConfigParameters import CConfigParameters
from ..Kernel.FileHanlders.Writer.CWriteT4BoundCond import CWriteT4BoundCond
"""
Usage:
        Converter_CLI.py conversion <p_nameT4File> <p_nameMCNPFile>
"""

def conversion(p_nameT4File, p_nameMCNPFile):
    with open(p_nameT4File, 'w') as ofile:
        dicVol = CWriteT4Geometry().m_writeT4Geometry(ofile)
        CWriteT4Composition().m_writeT4Composition(ofile)
        CWriteT4GeomComp(dicVol).m_writeT4GeomComp(ofile)
        CWriteT4BoundCond().m_writeT4BoundCond(ofile)

if __name__ == '__main__':
    config = CConfigParameters()
    t4_fname = config.m_readNameT4InputFile()
    mcnp_fname = config.m_readNameMCNPInputFile()
    conversion(t4_fname, mcnp_fname)

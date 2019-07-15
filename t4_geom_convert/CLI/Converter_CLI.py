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
# import cProfile
"""
Usage:
        Converter_CLI.py conversion <p_nameT4File> <p_nameMCNPFile>
"""

def conversion(p_nameT4File, p_nameMCNPFile):
    with open(p_nameT4File, 'w') as ofile:
        writegeom = CWriteT4Geometry()
        dicVol, mcnp_new_dict = writegeom.m_writeT4Geometry(ofile)
        CWriteT4Composition(mcnp_new_dict).m_writeT4Composition(ofile)
        CWriteT4GeomComp(dicVol, mcnp_new_dict).m_writeT4GeomComp(ofile)
        CWriteT4BoundCond().m_writeT4BoundCond(ofile)

def main():
    config = CConfigParameters()
    t4_fname = config.m_readNameT4InputFile()
    mcnp_fname = config.m_readNameMCNPInputFile()
    conversion(t4_fname, mcnp_fname)
    # cProfile.run('conversion(t4_fname, mcnp_fname)', 'ici.profile')

if __name__ == '__main__':
    main()

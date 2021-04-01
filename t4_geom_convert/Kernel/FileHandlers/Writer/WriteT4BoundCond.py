# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :

from ...BoundaryCondition.CConversionBoundaryCondition import CConversionBoundaryCondition


def writeT4BoundCond(dic_surf_mcnp, ofile):
    '''Method writing GeomComp to the T4 input file.'''
    d_boundCond = CConversionBoundaryCondition(
        dic_surf_mcnp).conversionBoundCond()
    if not d_boundCond:
        return
    ofile.write("\nBOUNDARY_CONDITION\n")
    ofile.write(str(len(d_boundCond)))
    ofile.write("\n")
    for k in d_boundCond.keys():
        p_typeOfBound = d_boundCond[k].typeOfBound
        ofile.write("ALL_COMPLETE %s %s\n" % (p_typeOfBound, k))
    ofile.write("END_BOUNDARY_CONDITION")
    ofile.write("\n")

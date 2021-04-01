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

from .CBoundCond import CBoundCond
from collections import OrderedDict


class CConversionBoundaryCondition:

    def __init__(self, dic_surf_mcnp):
        '''
        Constructor
        '''
        self.dic_surf_mcnp = dic_surf_mcnp

    def recuperateBoundaryCondition(self):
        '''
        Method constructing a dictionary with the id of the material as a key
        and the instance of CBoundCondT4 as a value
        '''
        d_boundCond = OrderedDict()
        for k, v in self.dic_surf_mcnp.items():
            if v[0][0].boundary_cond != '':
                if len(v) > 1:
                    msg = ('Boundary conditions on macrobodies are not '
                           'supported yet.')
                    raise NotImplementedError(msg)
                p_typeOfBC = v[0][0].boundary_cond
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

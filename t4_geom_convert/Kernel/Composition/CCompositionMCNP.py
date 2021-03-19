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

import math


class CCompositionMCNP:
    '''
    Class which permit to access precisely to the information of the part
    material of the block DATA
    '''

    def __init__(self, l_materialCompositionParameters):
        '''
        Constructor
        :param: l_materialCompositionParameters : list of composition of
        material with id of isotope and its abondance
        '''
        self.materialCompositionParameters = []
        i = 0
        while i < len(l_materialCompositionParameters):
            isotope = l_materialCompositionParameters[i]
            if '=' in isotope:
                # this is a keyword, skip it
                i += 1
                continue
            if "." in isotope:
                isotope = isotope.split(".")[0]
            fractionIsotope = l_materialCompositionParameters[i + 1]
            self.materialCompositionParameters.append((isotope,
                                                       fractionIsotope))
            i += 2

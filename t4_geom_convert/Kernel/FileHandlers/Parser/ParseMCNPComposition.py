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

from collections import OrderedDict
from MIP.geom.composition import get_material_composition
from ...Composition.CCompositionMCNP import CCompositionMCNP


def parseMCNPComposition(mcnpParser):
    '''
    :brief method which permit to recover the information of each line
    of the block SURFACE
    :return: dictionary which contains the ID of the materials as a key
    and as a value, a object from the class CCompositionMCNP
    '''
    compositionParser = get_material_composition(mcnpParser)
    dictComposition = OrderedDict()
    for k, v in list(compositionParser.items()):
        l_materialCompositionParameters = v
        dictComposition[k] = CCompositionMCNP(l_materialCompositionParameters)
    return dictComposition

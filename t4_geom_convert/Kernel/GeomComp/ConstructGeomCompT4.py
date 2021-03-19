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

from .CDictGeomCompT4 import CDictGeomCompT4
from .CGeomCompT4 import CGeomCompT4
from collections import defaultdict, OrderedDict


def constructGeomCompT4(dicVol, dic_cellMCNP):
    '''Method constructing a dictionary with the id of the material as a key
    and the instance of CGeomCompT4 as a value.'''
    dic_geomCompT4 = OrderedDict()
    dic_partialGeomComp = OrderedDict()
    obj_T4 = CDictGeomCompT4(dic_geomCompT4)
    for key, val in dicVol.items():
        if val.fictive:
            continue
        if val.idorigin:
            volID = val.idorigin[0][0]
        else:
            volID = key
        density = dic_cellMCNP[volID].density
        if density is None:
            materialName = dic_cellMCNP[volID].materialID
        else:
            materialName = dic_cellMCNP[volID].materialID + '_' + density
        if materialName not in dic_partialGeomComp:
            dic_partialGeomComp[materialName] = []
        dic_partialGeomComp[materialName].append(key)
    for key in dic_partialGeomComp.keys():
        numberOfCell = len(dic_partialGeomComp[key])
        listCell = dic_partialGeomComp[key]
        obj_T4[key] = CGeomCompT4(
            numberOfCell, " ".join(str(x) for x in listCell))
    return obj_T4.geomCompT4

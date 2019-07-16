# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateVolumeT4.py
'''

from collections import OrderedDict
from .CDictVolumeT4 import CDictVolumeT4
from .CDictCellMCNP import CDictCellMCNP
from .CCellConversion import CCellConversion
from .TreeFunctions import isLeaf
from .CUniverseDict import CUniverseDict
from ..Surface.CDictSurfaceMCNP import CDictSurfaceMCNP
from ..Configuration.CConfigParameters import CConfigParameters

class CIntermediateVolumeT4(object):
    '''
    :brief: Intermediate class which change the value of the dictionary from the
    conversion in instance of the Class CDictVolumeT4
    '''

    def __init__(self, dic_surface, dic_surfaceMCNP):
        '''
        Constructor
        '''
        self.dic_surface = dic_surface
        self.dic_surfaceMCNP = dic_surfaceMCNP

    def constructVolumeT4(self):
        '''
        :brief: method changing the tuple from CCellConversion in
        instance of the CVolumeT4 Class
        '''
        dic_cellT4 = OrderedDict()
        objT4 = CDictVolumeT4(dic_cellT4)
        mcnp_dict = CDictCellMCNP().d_cellMCNP
        mcnp_new_dict = mcnp_dict.copy()
        free_key = max(int(k) for k in mcnp_dict) + 1
        free_surf_key = max(
            max(int(k) for k in self.dic_surfaceMCNP) + 1,
            max(int(k) for k in self.dic_surface) + 1
            )
        surf_used = set()
        conv = CCellConversion(free_key, free_surf_key, objT4, self.dic_surface, self.dic_surfaceMCNP, mcnp_dict)
        listekeys = list(mcnp_dict)
        for key in mcnp_dict.keys():
            new_geom = conv.postOrderTraversalCompl(mcnp_dict[key].geometry)
            mcnp_dict[key].geometry = new_geom
        for key in mcnp_dict.keys():
            print('LATTICE', key, len(listekeys))
            print('*******************************************************************')
            conv.postOrderLattice(key, mcnp_new_dict)
        conv.new_cell_key = max(int(k) for k in mcnp_new_dict) + 1
        conv.new_surf_key = max(
            max(int(k) for k in self.dic_surfaceMCNP) + 1,
            max(int(k) for k in self.dic_surface) + 1
            )
        listekeys = list(mcnp_new_dict)
        dictUniverse = CUniverseDict(mcnp_new_dict).dictUniverse()
        for key in listekeys:
            print('FILL', key, len(listekeys))
            print('*******************************************************************')
            conv.postOrderTraversalFill(key, mcnp_new_dict,dictUniverse)
        conv.new_cell_key = max(int(k) for k in mcnp_new_dict) + 1
        conv.new_surf_key = max(
            max(int(k) for k in self.dic_surfaceMCNP) + 1,
            max(int(k) for k in self.dic_surface) + 1
            )
        for key, val in mcnp_new_dict.items():
            if val.importance != 0 and val.universe == 0 and val.fillid is None:
                root = val.geometry
                treeMaster = root
                tup = conv.postOrderTraversalFlag(treeMaster)
                replace = conv.postOrderTraversalReplace(tup)
                opt_tree = conv.postOrderTraversalOptimisation(replace)
                surf_used |= set(self.surfacesUsed(opt_tree))
                j = conv.postOrderTraversalConversion(opt_tree, val.idorigin)
                objT4.volumeT4[j].fictive = ''
                if j == key:
                    continue
                objT4.__setkey__(j, key)
                objT4.__setitem__(key, objT4.__getitem__(j))
                objT4.__delitem__(j)
        surf_used.add(100001)
        surf_used.add(100002)
        return dic_cellT4, surf_used, mcnp_new_dict


    def surfacesUsed(self, tree):
        if isLeaf(tree):
            return [abs(tree)]
        _id, _op, *args = tree
        result = [x for leaf in args for x in self.surfacesUsed(leaf)]
        return result

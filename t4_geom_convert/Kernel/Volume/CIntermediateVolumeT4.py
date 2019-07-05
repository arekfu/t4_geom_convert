# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CIntermediateVolumeT4.py
'''

from collections import OrderedDict
from ..Volume.CDictVolumeT4 import CDictVolumeT4
from ..Volume.CDictCellMCNP import CDictCellMCNP
from ..Volume.CCellConversion import CCellConversion
from ..Volume.CTreeMethods import CTreeMethods
from ..Surface.CDictSurfaceMCNP import CDictSurfaceMCNP
from ..Configuration.CConfigParameters import CConfigParameters
from ..Volume.CUniverseDict import CUniverseDict

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

    def m_constructVolumeT4(self):
        '''
        :brief: method changing the tuple from CCellConversionMCNPToT4 in
        instance of the CVolumeT4 Class
        '''
#         dic_test = dict()
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
#             print('key',key)
            new_geom = conv.m_postOrderTraversalCompl(mcnp_dict[key].geometry)
            mcnp_dict[key].geometry = new_geom
        for key in mcnp_dict.keys():
            print('LATTICE', key, len(listekeys))
            print('*******************************************************************')
            conv.m_postOrderLattice(key, mcnp_new_dict)
        conv.new_cell_key = max(int(k) for k in mcnp_new_dict) + 1
        conv.new_surf_key = max(
            max(int(k) for k in self.dic_surfaceMCNP) + 1,
            max(int(k) for k in self.dic_surface) + 1
            )
        listekeys = list(mcnp_new_dict)
        dictUniverse = CUniverseDict(mcnp_new_dict).m_dictUniverse()
        for key in listekeys:
            print('FILL', key, len(listekeys))
            print('*******************************************************************')
            conv.m_postOrderTraversalFill(key, mcnp_new_dict,dictUniverse)
        conv.new_cell_key = max(int(k) for k in mcnp_new_dict) + 1
        conv.new_surf_key = max(
            max(int(k) for k in self.dic_surfaceMCNP) + 1,
            max(int(k) for k in self.dic_surface) + 1
            )
        for key, val in mcnp_new_dict.items():
#             print('volume', key, val.geometry, val.importance, val.universe)
            if val.importance != 0 and val.universe == 0 and val.fillid is None:
#                 dic_test[key] = dict()
                root = val.geometry
                treeMaster = root
                tup = conv.m_postOrderTraversalFlag(treeMaster)
#                 print('tup',tup)
                replace = conv.m_postOrderTraversalReplace(tup)
#                 print('replace', replace)
                opt_tree = conv.m_postOrderTraversalOptimisation(replace)
#                 print('opt_tree', opt_tree)
                surf_used |= set(self.m_surfacesUsed(opt_tree))
                j = conv.m_postOrderTraversalConversion(opt_tree, val.idorigin)
                objT4.volumeT4[j].fictive = ''
                if j == key:
                    continue
                objT4.__setkey__(j, key)
                objT4.__setitem__(key, objT4.__getitem__(j))
#                 print('j',j, key)
                objT4.__delitem__(j)
#         print(dic_cellT4)
        surf_used.add(100001)
        surf_used.add(100002)
        return dic_cellT4, surf_used, mcnp_new_dict


    def m_surfacesUsed(self, tree):
        if CTreeMethods().m_isLeaf(tree):
            #print('leaf', tree)
            return [abs(tree)]
        _id, _op, *args = tree
        result = [x for leaf in args for x in self.m_surfacesUsed(leaf)]
        #print('result', tree, result)  
        return result
    
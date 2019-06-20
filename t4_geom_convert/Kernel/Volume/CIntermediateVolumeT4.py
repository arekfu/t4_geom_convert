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


class CIntermediateVolumeT4(object):
    '''
    :brief: Intermediate class which change the value of the dictionary from the
    conversion in instance of the Class CDictVolumeT4
    '''

    def __init__(self, dic_surface):
        '''
        Constructor
        '''
        self.dic_surface = dic_surface

    def m_constructVolumeT4(self):
        '''
        :brief: method changing the tuple from CCellConversionMCNPToT4 in
        instance of the CVolumeT4 Class
        '''
        dic_test = dict()
        dic_cellT4 = OrderedDict()
        objT4 = CDictVolumeT4(dic_cellT4)
        dicSurfaceMCNP = CDictSurfaceMCNP().d_surfaceMCNP
        mcnp_dict = CDictCellMCNP().d_cellMCNP
        mcnp_new_dict = mcnp_dict.copy()
        free_key = max(int(k) for k in mcnp_dict) + 1
        listekeys = []
        surf_used = set()
        conv = CCellConversion(free_key, objT4, self.dic_surface, dicSurfaceMCNP, mcnp_dict)
        for i in mcnp_dict.keys():
            listekeys.append(i)
        for i,key in enumerate(listekeys):
            print('FILL', key, ' ', i, len(listekeys))
            print('*******************************************************************')
            conv.m_postOrderTraversalFill(key, mcnp_new_dict)
        for key, val in mcnp_new_dict.items():
            print('volume', key, val.importance, val.universe)
            if val.importance != 0 and val.universe == 0 and val.fillid is None:
                dic_test[key] = dict()
                root = val.geometry
                treeMaster = root
                tup = conv.m_postOrderTraversalFlag(treeMaster)
                replace = conv.m_postOrderTraversalReplace(tup)
                opt_tree = conv.m_postOrderTraversalOptimisation(replace)
                surf_used |= set(self.m_surfacesUsed(opt_tree))
                j = conv.m_postOrderTraversalConversion(opt_tree, val.idorigin)
                objT4.volumeT4[j].fictive = ''
                objT4.__setkey__(j, key)
                objT4.__setitem__(key, objT4.__getitem__(j))
                objT4.__delitem__(j)
                free_key = conv.i
        return dic_cellT4, surf_used


    def m_surfacesUsed(self, tree):
        if CTreeMethods().m_isLeaf(tree):
            print('leaf', tree)
            return [abs(tree)]
        _id, _op, *args = tree
        result = [x for leaf in args for x in self.m_surfacesUsed(leaf)]
        print('result', tree, result)  
        return result

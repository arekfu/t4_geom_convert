# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CCellConversion.py
'''

from ..Volume.CDictVolumeT4 import CDictVolumeT4
from ..Volume.CDictCellMCNP import CDictCellMCNP
from ..Volume.CTreeMethods import CTreeMethods
from ..Volume.CVolumeT4 import CVolumeT4

class CCellConversion(object):
    '''
    :brief: Class which contains methods to convert the Cell of MCNP in T4 Volume
    '''

    def __init__(self, int_i, d_dictClassT4):
        '''
        Constructor
        :param: int_i : id of the volume created
        :param: d_dictClassT4 : dictionary filled by the methods and which
        contains volumes informations
        '''
        self.i = int_i
        self.dictClassT4 = d_dictClassT4

    def m_conversionEQUA(self, list_surface, fictive):
        '''
        :brief: method converting a list of if of surface and return a tuple with the
        informations of the volume EQUA T4
        '''

        str_equaMinus = ''
        str_equaPlus = ''
        i_minus = 0
        i_plus = 0
        for elt in list_surface:
            if '-' in str(elt):
                i_minus += 1
                elt = int(elt)
                elt = abs(elt)
                str_equaMinus = str_equaMinus + str(elt) + ' '
            else:
                i_plus += 1
                str_equaPlus = str_equaPlus + str(elt) + ' '
        str_equaPlus = 'PLUS'+ ' ' + str(i_plus) + ' ' + str_equaPlus
        str_equaMinus = 'MINUS'+ ' ' + str(i_minus) + ' ' + str_equaMinus
        str_equa = str_equaPlus + ' ' + str_equaMinus
        if fictive == False:
            s_fictive = ''
        if fictive == True:
            s_fictive = 'FICTIVE'
        tuple_final = 'EQUA', str_equa, s_fictive
        return(tuple_final)

    def m_conversionINTUNION(self, op, *ids, fictive):
        '''
        :brief: method analyze the type of conversion needed between a T4 INTERSECTION
        and a T4 UNION and return a tuple with the information of the T4 VOLUME
        '''

        if op == '*':
            opT4 = 'INTE'
        if op == ':':
            opT4 = 'UNION'
        if fictive == False:
            s_fictive = ''
        if fictive == True:
            s_fictive = 'FICTIVE'
        s_param = str(len(ids)) + ' ' + ' '.join(str(a_id) for a_id in ids)
        tuple_final = opT4, s_param, s_fictive
        return tuple_final

    def m_postOrderTraversalFlag(self, p_tree):
        '''
        :brief: method which take a tree and return a tuple of tuple \
        with flag to decorate each tree in the tree
        '''

        if not CTreeMethods().m_isLeaf(p_tree):
            op, left, right = p_tree
            new_l = self.m_postOrderTraversalFlag(left)
            new_r = self.m_postOrderTraversalFlag(right)
            self.i += 1
            new_tree = [self.i, op, new_l, new_r]
            return new_tree
        else:
            return p_tree

    def m_postOrderTraversalConversion(self, p_tree):
        '''
        :brief: method which take the tree create by m_postOrderTraversalFlag\
        and filled a dictionary (of CVolumeT4 instance)
        '''

        if CTreeMethods().m_isInterSurface(p_tree):
            p_id, op = p_tree[0:2]
            children = p_tree[2:]
            tupEQUA = self.m_conversionEQUA(children, fictive=True)
            opT4, param, fict = tupEQUA
            self.dictClassT4.__setitem__(p_id, CVolumeT4(opT4, param, fict))
            return p_id
        if CTreeMethods().m_isLeaf(p_tree):
            p_id = abs(p_tree) + self.i * 10
            tupEQUA = self.m_conversionEQUA([p_tree], fictive=True)
            opT4, param, fict = tupEQUA
            self.dictClassT4[p_id] = CVolumeT4(opT4, param, fict)
            return p_id
        else:
            print(p_tree)
            p_id, op, *args = p_tree
            arg_ids = [self.m_postOrderTraversalConversion(arg) for arg in args]
            tupOPER = self.m_conversionINTUNION(op, *arg_ids, fictive=True)
            opT4, param, fict = tupOPER
            self.dictClassT4.__setitem__(p_id, CVolumeT4(opT4, param, fict))
            return p_id

    def m_postOrderTraversalOptimisation(self, p_tree):
        '''
        :brief: method which permit to optimize the course of the cells MCNP
        '''

        if CTreeMethods().m_isLeaf(p_tree):
            return p_tree
        p_id, op, left, right = p_tree
        new_left = self.m_postOrderTraversalOptimisation(left)
        new_right = self.m_postOrderTraversalOptimisation(right)
        new_node = [p_id, op]
        for node in [new_left, new_right]:
            if CTreeMethods().m_isInterSurface(node) and op == '*':
                new_node.extend(node[2:])
            else:
                new_node.append(node)
        return new_node

dic_test = dict()
dic_cellT4 = dict()
objT4 = CDictVolumeT4(dic_cellT4)
for key, val in CDictCellMCNP().d_cellMCNP.items():
    dic_test[key] = dict()
    root = val.geometry
    tree = root
    obj_conversion = CCellConversion(key*1000, objT4)
    tup = obj_conversion.m_postOrderTraversalFlag(tree)
    opt_tree = obj_conversion.m_postOrderTraversalOptimisation(tup)
    print('**********', opt_tree)
    j = obj_conversion.m_postOrderTraversalConversion(opt_tree)
    objT4.__setkey__(j, key)
    objT4.__setitem__(key, objT4.__getitem__(j))
for key, value in dic_cellT4.items():
    print(key, dic_cellT4[key].operator, dic_cellT4[key].param)

#     if l != []:
#         tupEqua = CCellConversion(key*1000,objT4).m_conversionEQUA(l, fictive=True)
#         opT4, param, fict = tupEqua
#         print(i,tupEqua)
#         CCellConversion(key*1000,objT4).dictClassT4.__setitem__(i, CVolumeT4(opT4, param, fict))
# for key in dic_cellT4.keys():
#     print(key, dic_cellT4[key].operator, dic_cellT4[key].param)

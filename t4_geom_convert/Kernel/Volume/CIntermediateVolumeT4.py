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


class CIntermediateVolumeT4(object):
    '''
    :brief: Intermediate class which change the value of the dictionary from the
    conversion in instance of the Class CDictVolumeT4
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def m_constructVolumeT4(self):
        '''
        :brief: method changing the tuple from CCellConversionMCNPToT4 in
        instance of the CVolumeT4 Class
        '''
        dic_test = dict()
        dic_cellT4 = OrderedDict()
        objT4 = CDictVolumeT4(dic_cellT4)
        for key, val in CDictCellMCNP().d_cellMCNP.items():
            dic_test[key] = dict()
            root = val.geometry
            tree = root
            tup = CCellConversion(key*1000, objT4).m_postOrderTraversalFlag(tree)
            print(tup)
            opt_tree = CCellConversion(key*1000, objT4).m_postOrderTraversalOptimisation(tup)
            j = CCellConversion(key*1000, objT4).m_postOrderTraversalConversion(opt_tree)
            objT4.volumeT4[j].fictive = ''
            objT4.__setkey__(j, key)
            objT4.__setitem__(key, objT4.__getitem__(j))
            objT4.__delitem__(j)
        return dic_cellT4

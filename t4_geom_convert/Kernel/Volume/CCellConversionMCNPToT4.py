# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CCellConversionMCNPToT4.py
'''
from ..Volume.CDictCellMCNP import CDictCellMCNP
from ..Volume.CDictVolumeT4 import CDictVolumeT4
import re
from ...MIP import geom
class CCellConversionMCNPToT4(object):
    '''
    :brief: Class with method for converting the cell of MCNP in volume for T4
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def m_conversionCellMCNPToT4(self):
        
        '''
        :brief: method filling a dictionary of the conversion of the MCNP Cells 
        :return: dictionary with in key th id of the volume and in value the tuple corresponding to the id
        '''
        
        dic_cellT4 = dict()
        objT4 = CDictVolumeT4(dic_cellT4)
        for key,val in CDictCellMCNP().d_cellMCNP.items() :
#             print(key)
            AST = val.m_evaluateASTMCNP()
            value = self.m_conversionASTInVolumeT4(key, AST)
            objT4.__setitem__(key, value)
        return dic_cellT4 
            
    def m_conversionASTInVolumeT4(self, key, AST):
        '''
        :brief: method doing operation to convert a cell MCNP into a volume T4
        :return: tuple with the information of the cell MCNP translate 
        '''
        list_AST = AST.split(')')
        list_AST = list_AST[0:len(list_AST)- 1]
        list_EQUA = []
        list_UNION = []
        list_equaMinus = []
        list_equaPlus = []
        list_unionPlus = []
        list_unionMinus = []
            
        for element in list_AST:
            if '*' in element:
                list_EQUA = list_EQUA + re.findall(r'-?\d+\.?\d*', element)
            if ':' in element:
                list_UNION = list_UNION + re.findall(r'-?\d+\.?\d*', element)
        if list_EQUA != [] :
            for elt in list_EQUA:
                if '-' in elt:
                    list_equaMinus = list_equaMinus + re.findall('\d+',elt)
                else:
                    list_equaPlus = list_equaPlus + re.findall('\d+',elt)
            tuple_equaPlus = 'PLUS',len(list_equaPlus), list_equaPlus
            tuple_equaMinus = 'MINUS', len(list_equaMinus), list_equaMinus
            tuple_final = 'EQUA', tuple_equaPlus, tuple_equaMinus
        if list_UNION != [] :
            for elt in list_UNION:
                if '-' in elt:
                    list_unionMinus = list_unionMinus + re.findall('\d+',elt)
                else:
                    list_unionPlus = list_unionPlus + re.findall('\d+',elt)
            tuple_unionPlus = 'PLUS',len(list_unionPlus), list_unionPlus
            tuple_unionMinus = 'MINUS', len(list_unionMinus), list_unionMinus
            tuple_final = 'UNION', tuple_unionPlus, tuple_unionMinus
        return key, tuple_final
    
# def m_isLeaf(tree):
#          
#     if isinstance(tree, geom.semantics.GeomExpression) == True:
#         return False
#     elif isinstance(tree, geom.semantics.Surface) == True:
#         return True

# def m_conversionEQUA(list_surface, fictive):
#     str_equaMinus = ''
#     str_equaPlus = ''
#     i_minus = 0
#     i_plus = 0
#     for elt in list_surface:
#         if '-' in str(elt):
#             i_minus +=1
#             elt = int(elt)
#             elt = abs(elt)
#             str_equaMinus = str_equaMinus + str(elt)
#         else:
#             i_plus += 1
#             str_equaPlus = str_equaPlus + str(elt)
#     tuple_equaPlus = 'PLUS',i_plus, str_equaPlus
#     tuple_equaMinus = 'MINUS', i_minus, str_equaMinus
#     if fictive == False:
#         s_fictive='' 
#     if fictive == True:
#         s_fictive = 'FICTIVE'
#     tuple_final = 'EQUA', tuple_equaPlus, tuple_equaMinus, s_fictive
#     return(tuple_final)

def m_conversionUNION(list_fictiveVolumeID, fictive):
    str_listFictiveVolume = ''
    for elt in list_fictiveVolumeID:
        str_listFictiveVolume = str_listFictiveVolume + ' ' + str(elt)
    if fictive == False:
        s_fictive='' 
    if fictive == True:
        s_fictive = 'FICTIVE'
    tuple_final = 'UNION', len(list_fictiveVolumeID),str_listFictiveVolume, s_fictive
    return tuple_final

def m_conversionINTE(list_fictiveVolumeID, fictive):
    str_listFictiveVolume = ''
    for elt in list_fictiveVolumeID:
        str_listFictiveVolume = str_listFictiveVolume + ' ' + str(elt)
    if fictive == False:
        s_fictive='' 
    if fictive == True:
        s_fictive = 'FICTIVE'
    tuple_final = 'INTE', len(list_fictiveVolumeID),str_listFictiveVolume, s_fictive
    return tuple_final
         
def m_postOrderTraversal(key, dico, tree):
    i = 0
    if m_isLeaf(tree) == False:
        
        op,left,right = tree 
        m_postOrderTraversal(key+1, dico, left)
        m_postOrderTraversal(key+2, dico, right)
        dico[key] = (op,left,right)
        i= i+1
        #print(op,left,right)
        
            
# p = CCellConversionMCNPToT4().m_conversionCellMCNPToT4()
# for key,val in p.items():
#     operator, plus, minus = val
#     name, number, liste = plus  
#     print(name, number, liste)
dic_test = dict()  
dic_cellT4 = dict()
objT4 = CDictVolumeT4(dic_cellT4)    
for key,val in CDictCellMCNP().d_cellMCNP.items():
    dic_test[key]=dict()
    root = val.geometry
    tree = root
    m_postOrderTraversal(key*1000, dic_test[key], tree)
for key in dic_test.keys():
    init_key = list(dic_test[key])[-1]
    operator, left_subBranch, right_subBranch = dic_test[key][init_key]
    if operator == '*':
        list_surface = [left_subBranch,right_subBranch]
        tup = m_conversionEQUA(list_surface, fictive=True)
        objT4.__setitem__(init_key, tup)
#         print(tup)
    if operator == ':':
        tup1 = m_conversionEQUA([left_subBranch], fictive = True)
        keyF1=init_key*10
        objT4.__setitem__(keyF1, tup1)
        keyF2 = keyF1+1
        tup2 = m_conversionEQUA([right_subBranch], fictive = True)
        objT4.__setitem__(keyF2, tup2)
        liste_fictiveVolumeID = [keyF1,keyF2]
        tupf = m_conversionUNION(liste_fictiveVolumeID,fictive=True)
        objT4.__setitem__(init_key, tupf)
#         print(tup1)
#         print(tup2)
#         print(tupf)
    len_tree = len(list(dic_test[key]))
    for k in reversed(list(dic_test[key])[0:len_tree-1]):
        operator, left_subBranch, right_subBranch = dic_test[key][k]
        if operator == '*':
            if m_isLeaf(right_subBranch) == True:
                if m_isLeaf(left_subBranch)== False:
                    tup1 = m_conversionEQUA([right_subBranch], fictive = True)
                    keyF1=k*10
                    objT4.__setitem__(keyF1, tup1)
                    liste_fictiveVolumeID = [keyF1,init_key]
                    tupf = m_conversionINTE(liste_fictiveVolumeID,fictive=True)
                    objT4.__setitem__(k, tupf)
                    init_key = k   
#                 print('INTEEEE',tup1) 
#                 print('INTEEEEEE',tupf)
                if m_isLeaf(left_subBranch)==True:
                    list_surface = [left_subBranch,right_subBranch]
                    tup = m_conversionEQUA(list_surface, fictive=True)
                    objT4.__setitem__(k, tup)
                    init_key = k 
            if m_isLeaf(right_subBranch)==False:
                if m_isLeaf(left_subBranch)== False:
                    liste_fictiveVolumeID = [k-2,init_key]
                    tupf = m_conversionINTE(liste_fictiveVolumeID,fictive=True)
                    objT4.__setitem__(k, tupf)
                    init_key = k
        if operator ==':':
            if m_isLeaf(right_subBranch) == True:
                if m_isLeaf(left_subBranch)== False:
                    tup1 = m_conversionEQUA([right_subBranch], fictive = True)
                    keyF1=k*10
                    objT4.__setitem__(keyF1, tup1)
                    liste_fictiveVolumeID = [keyF1,init_key]
                    tupf = m_conversionUNION(liste_fictiveVolumeID,fictive=True)
                    objT4.__setitem__(k, tupf)
                    init_key = k   
#                 print('INTEEEE',tup1) 
#                 print('INTEEEEEE',tupf)
                if m_isLeaf(left_subBranch)==True:
                    list_surface = [left_subBranch,right_subBranch]
                    tup = m_conversionEQUA(list_surface, fictive=True)
                    objT4.__setitem__(k, tup)
                    init_key = k 
            if m_isLeaf(right_subBranch)==False:
                if m_isLeaf(left_subBranch)== False:
                    liste_fictiveVolumeID = [k-2,init_key]
                    tupf = m_conversionUNION(liste_fictiveVolumeID,fictive=True)
                    objT4.__setitem__(k, tupf)
                    init_key = k
            
for k in objT4.volumeT4.keys():
    print(k, objT4.volumeT4[k])
            
####################################################
#    print(root)
#     if m_isLeaf(root) == True:
#         print(root)
#         
#     else:
#         left_tree = root[1]
#         right_tree = root[2]
#         list_leftBranch = []
#         while m_isLeaf(left_tree) == False:
#             list_leftBranch.append(left_tree)
#             left_tree = left_tree[1]
#         print(list_leftBranch)
#         for element in list_leftBranch:
#             print(type(element))
            
#########################################################################""   
    
#     if m_isLeaf(tree)==True:
#         list_surface = [tree[1],tree[2]]
#         if str(tree[0]) == '*' :
#             tup = m_conversionEQUA(list_surface, fictive = False)
#             objT4.__setitem__(key, tup)
#             print(tup)
#         if str(tree[0]) == ':' :
#             keyF1 = key * 10000
#             tup1 = m_conversionEQUA([tree[1]], fictive = False)
#             objT4.__setitem__(keyF1, tup1)
#             keyF2 = keyF1 + 1
#             tup2 = m_conversionEQUA([tree[2]], fictive = False)
#             objT4.__setitem__(keyF2, tup2)
#             liste_fictiveVolumeID = [keyF1,keyF2]
#             tupf = m_conversionUNION(liste_fictiveVolumeID,fictive=False)
#             objT4.__setitem__(key, tupf)
#              
#      
#     else:
#             
#         while m_isLeaf(tree) == False:
#             
#             operator, left_subBranch, right_subBranch = tree
#             if m_isLeaf(left_subBranch) == True: 
#                 if operator == '*':
#                     list_surface = [left_subBranch,right_subBranch]
#                     tup = m_conversionEQUA(list_surface, fictive=True)
#                     keyF=key*10000
#                     objT4.__setitem__(keyF, tup)
#                     print(tup)
#                     break
#                 if operator == ':':
#                     keyF1 = key * 10000
#                     tup1 = m_conversionEQUA([left_subBranch], fictive = True)
#                     objT4.__setitem__(keyF1, tup1)
#                     keyF2 = keyF1 + 1
#                     tup2 = m_conversionEQUA([right_subBranch], fictive = True)
#                     objT4.__setitem__(keyF2, tup2)
#                     liste_fictiveVolumeID = [keyF1,keyF2]
#                     keyF3 = keyF2 + 1
#                     tupf = m_conversionUNION(liste_fictiveVolumeID,fictive=True)
#                     objT4.__setitem__(keyF3, tupf)
#                     print(tup1)
#                     print(tup2)
#                     print(tupf)
#                     break
#             else :
#                 past_tree = tree
#                 tree = left_subBranch
#         while m_isLeaf(past_tree) == False:
#             print(past_tree)
#             operator, left_subBranch, right_subBranch = past_tree
#             print(operator)
#             print(left_subBranch)
#             print(right_subBranch)    
#             if m_isLeaf(right_subBranch) == True: 
#                 if operator == '*':
#                     list_surface = [right_subBranch[1],right_subBranch[2]]
#                     tup = m_conversionEQUA(list_surface, fictive=True)
#                     keyF=key*10000
#                     objT4.__setitem__(keyF, tup)
#                     break
#                 if operator == ':':
#                     keyF1 = key * 10000
#                     tup1 = m_conversionEQUA([right_subBranch[1]], fictive = True)
#                     objT4.__setitem__(keyF1, tup1)
#                     keyF2 = keyF1 + 1
#                     tup2 = m_conversionEQUA([right_subBranch[2]], fictive = True)
#                     objT4.__setitem__(keyF2, tup2)
#                     liste_fictiveVolumeID = [keyF1,keyF2]
#                     keyF3 = keyF2 + 1
#                     tupf = m_conversionUNION(liste_fictiveVolumeID,fictive=True)
#                     objT4.__setitem__(keyF3, tupf)
#                     break
#             else :
#                 past_tree_bis = past_tree
#                 past_tree = right_subBranch
            
                 

            
            
            
        



    
        
        
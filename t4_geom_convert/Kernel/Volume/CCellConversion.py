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
from ...MIP.geom.semantics import GeomExpression, Surface
from ..Configuration.CConfigParameters import CConfigParameters
from ..Volume.CUniverseDict import CUniverseDict
from t4_geom_convert.MIP.geom.transforms import to_cos
from ..Transformation.CTransformationFonction import CTransformationFonction
from ..Transformation.CConversionSurfaceTransformed import CConversionSurfaceTransformed
from ..Surface.CSurfaceT4 import CSurfaceT4

class CCellConversion(object):
    '''
    :brief: Class which contains methods to convert the Cell of MCNP in T4 Volume
    '''

    def __init__(self, int_i, d_dictClassT4, d_dictSurfaceT4, d_dicSurfaceMCNP, d_dicCellMCNP):
        '''
        Constructor
        :param: int_i : id of the volume created
        :param: d_dictClassT4 : dictionary filled by the methods and which
        contains volumes informations
        '''
        self.i = int_i
        self.dictClassT4 = d_dictClassT4
        self.dictSurfaceT4 = d_dictSurfaceT4
        self.dicSurfaceMCNP = d_dicSurfaceMCNP
        self.dicCellMCNP = d_dicCellMCNP
        self.inputMCNP = CConfigParameters().m_readNameMCNPInputFile()
        self.dictUniverse = CUniverseDict(self.dicCellMCNP).m_dictUniverse()

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
        if i_plus == 0 and i_minus != 0:
            str_equaPlus = ''
        if i_minus == 0 and i_plus != 0:
            str_equaMinus = ''
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
        keyS = 100000
        if op == '*':
            opT4 = 'EQUA INTE'
        if op == ':':
            tupleForEqua = self.m_conversionEQUA([keyS+1, -(keyS+2)], fictive=True)
            tupleEquaFinal = tupleForEqua[0:2]
            opT4 = tupleEquaFinal[0] + ' ' + tupleEquaFinal[1] + 'UNION'
        if fictive == False:
            s_fictive = ''
        if fictive == True:
            s_fictive = 'FICTIVE'
        s_param = str(len(ids)) + ' ' + ' '.join(str(a_id) for a_id in ids)
        tuple_final = opT4, s_param, s_fictive
        print(tuple_final)
        return tuple_final

    def m_postOrderTraversalFill(self, key, mcnp_new_dict):

        if self.dicCellMCNP[key].fillid is not None:
            new_cells = []
            cells_to_process = [] 
            mcnp_key_geom = mcnp_new_dict[key].geometry
            if mcnp_new_dict[key].costr:
                print('first fill tr', mcnp_new_dict[key].filltr)
                mcnp_new_dict[key].filltr[3:] = list(map(to_cos, mcnp_new_dict[key].filltr[3:]))
                mcnp_new_dict[key].costr = False
                print('second fill tr', mcnp_new_dict[key].filltr)
            mcnp_key_filltr = mcnp_new_dict[key].filltr
            for element in self.dictUniverse[int(self.dicCellMCNP[key].fillid)]:
                cells_to_process.extend(self.m_postOrderTraversalFill(element, mcnp_new_dict))
            for element in cells_to_process:
                mcnp_element_geom = mcnp_new_dict[element].geometry
                mcnp_new_dict_materialID = mcnp_new_dict[element].materialID
                new_key = element*10000 + key
                mcnp_new_dict[new_key] = mcnp_new_dict[key].m_copy()
                mcnp_new_dict[new_key].fillid = None
                mcnp_new_dict[new_key].materialID = mcnp_new_dict_materialID
                mcnp_new_dict[new_key].idorigin = mcnp_new_dict[element].idorigin.copy()
                mcnp_new_dict[new_key].idorigin.append(element)
                print('idorigin', key, new_key, element, mcnp_new_dict[key].idorigin, mcnp_new_dict[new_key].idorigin)
                print('idorigin', id(mcnp_new_dict[key]), id(mcnp_new_dict[new_key]))
                tree = self.m_postOrderTraversalTransform(mcnp_element_geom, mcnp_key_filltr)
                mcnp_new_dict[new_key].geometry = ('*', mcnp_key_geom, tree)
                new_cells.append(new_key)
            return new_cells
        else:
            # mcnp_new_dict[key] = self.dicCellMCNP[key].m_copy()
            return [key]


    def m_postOrderTraversalFlag(self, p_tree):
        '''
        :brief: method which take a tree and return a tuple of tuple \
        with flag to decorate each tree in the tree
        '''

        if not CTreeMethods().m_isLeaf(p_tree):
            op, *args = p_tree
            new_args = [self.m_postOrderTraversalFlag(node) for node in args]
            self.i += 1
            new_tree = [self.i, op]
            new_tree.extend(new_args)
            return new_tree
        else:
            return p_tree
    
    def m_postOrderTraversalTransform(self, p_tree, p_transf):
        print('p_tree', p_tree)
        if CTreeMethods().m_isLeaf(p_tree):
            surfaceObject = self.dicSurfaceMCNP[abs(p_tree)]
            if not p_transf:
                return p_tree
            print('p_transf', p_transf)
            p_boundCond, p_typeSurface, l_paramSurface \
             = surfaceObject.boundaryCond,\
             surfaceObject.typeSurface, surfaceObject.paramSurface
            surfaceObject = CTransformationFonction().m_transformation(p_boundCond, p_transf, p_typeSurface, l_paramSurface)
            (typeSurface, param) = CConversionSurfaceTransformed().m_conversion(surfaceObject)
            new_key = max(int(k) for k in self.dictSurfaceT4) + 1
            self.dicSurfaceMCNP[new_key] = surfaceObject
            self.dictSurfaceT4[new_key] = (CSurfaceT4(typeSurface.name, param),[])
            print('dicSurfT4', new_key, [(typeSurface, param)])
            return new_key if p_tree >= 0 else -new_key
        else:
            op, *args = p_tree
            new_args = [self.m_postOrderTraversalTransform(node, p_transf) for node in args]
            new_tree = [op]
            new_tree.extend(new_args)
            return new_tree
    
    def m_postOrderTraversalConversion(self, p_tree, idorigin):
        '''
        :brief: method which take the tree create by m_postOrderTraversalFlag\
        and filled a dictionary (of CVolumeT4 instance)
        '''

        if CTreeMethods().m_isInterSurface(p_tree):
            p_id, op = p_tree[0:2]
            children = p_tree[2:]
            tupEQUA = self.m_conversionEQUA(children, fictive=True)
            opT4, param, fict = tupEQUA
            self.dictClassT4.__setitem__(p_id, CVolumeT4(opT4, param, fict,idorigin))
            return p_id
        if CTreeMethods().m_isLeaf(p_tree):
            self.i += 1
            p_id = self.i
            tupEQUA = self.m_conversionEQUA([p_tree], fictive=True)
            opT4, param, fict = tupEQUA
            self.dictClassT4[p_id] = CVolumeT4(opT4, param, fict, idorigin)
            return p_id
        else:
            p_id, op, *args = p_tree
            arg_ids = [self.m_postOrderTraversalConversion(node, idorigin) for node in args]
            tupOPER = self.m_conversionINTUNION(op, *arg_ids, fictive=True)
            opT4, param, fict = tupOPER
            self.dictClassT4.__setitem__(p_id, CVolumeT4(opT4, param, fict, idorigin))
            return p_id

    def m_postOrderTraversalOptimisation(self, p_tree):
        '''
        :brief: method which permit to optimize the course of the cells MCNP
        '''

        if CTreeMethods().m_isLeaf(p_tree):
            return p_tree
        p_id, op, *args = p_tree
        new_args = [self.m_postOrderTraversalOptimisation(node) for node in args]
        new_node = [p_id, op]
        for node in new_args:
            if CTreeMethods().m_isIntersection(node) and op == '*':
                new_node.extend(node[2:])
            elif CTreeMethods().m_isUnion(node) and op == ':':
                new_node.extend(node[2:])
            else:
                new_node.append(node)
        return new_node

    def m_postOrderTraversalReplace(self, p_tree):
        if not CTreeMethods().m_isLeaf(p_tree):
            # print('replace: node {} is not a leaf'.format(p_tree))
            p_id, op, *args = p_tree
            new_tree = [p_id, op]
            new_tree.extend(self.m_postOrderTraversalReplace(node) for node in args)
            # print('replace: new_tree = {}'.format(new_tree))
            return new_tree

        abs_id = abs(p_tree)
        if abs_id not in self.dictSurfaceT4:
            # print('replace: node {} is not in dict'.format(p_tree))
            return p_tree

        surfT4 = self.dictSurfaceT4[abs_id]
        if not surfT4[1]:
            # print('replace: node {} has an empty list: {}'.format(p_tree, surfT4))
            return p_tree

        self.i += 1
        if p_tree < 0:
            new_node = [self.i, '*', p_tree]
            new_node.extend(Surface(surf) for surf in surfT4[1])
        else:
            new_node = [self.i, ':', p_tree]
            new_node.extend(Surface(-surf) for surf in surfT4[1])
        print('replace: replacing {} with {}'.format(p_tree, new_node))
        return GeomExpression(new_node)

# dic_test = dict()
# dic_cellT4 = dict()
# objT4 = CDictVolumeT4(dic_cellT4)
# for key, val in CDictCellMCNP().d_cellMCNP.items():
#     dic_test[key] = dict()
#     root = val.geometry
#     tree = root
#     obj_conversion = CCellConversion(key*1000, objT4)
#     tup = obj_conversion.m_postOrderTraversalFlag(tree)
#     opt_tree = obj_conversion.m_postOrderTraversalOptimisation(tup)
#     print('**********', opt_tree)
#     j = obj_conversion.m_postOrderTraversalConversion(opt_tree)
#     objT4.__setkey__(j, key)
#     objT4.__setitem__(key, objT4.__getitem__(j))
# for key, value in dic_cellT4.items():
#     print(key, dic_cellT4[key].operator, dic_cellT4[key].param)

#     if l != []:
#         tupEqua = CCellConversion(key*1000,objT4).m_conversionEQUA(l, fictive=True)
#         opT4, param, fict = tupEqua
#         print(i,tupEqua)
#         CCellConversion(key*1000,objT4).dictClassT4.__setitem__(i, CVolumeT4(opT4, param, fict))
# for key in dic_cellT4.keys():
#     print(key, dic_cellT4[key].operator, dic_cellT4[key].param)

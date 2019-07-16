# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CCellConversion.py
'''

from MIP.geom.semantics import GeomExpression, Surface
from MIP.geom.transforms import to_cos, normalize_transform
from MIP.geom.forcad import mcnp2cad
from MIP.geom.main import extract_surfaces_list

from .CDictVolumeT4 import CDictVolumeT4
from .CDictCellMCNP import CDictCellMCNP
from .TreeFunctions import isLeaf, isIntersection, isUnion
from .CVolumeT4 import CVolumeT4
from .CUniverseDict import CUniverseDict
from ..Configuration.CConfigParameters import CConfigParameters
from ..Transformation.CTransformationFonction import CTransformationFonction
from ..Transformation.CConversionSurfaceTransformed import CConversionSurfaceTransformed
from ..Surface.CSurfaceT4 import CSurfaceT4
from ..Surface.ESurfaceTypeMCNP import mcnp_to_mip
from math import fabs, sqrt

class CCellConversion(object):
    '''
    :brief: Class which contains methods to convert the Cell of MCNP in T4 Volume
    '''

    def __init__(self, int_cell, int_surf, d_dictClassT4, d_dictSurfaceT4, d_dicSurfaceMCNP, d_dicCellMCNP):
        '''
        Constructor
        :param: int_i : id of the volume created
        :param: d_dictClassT4 : dictionary filled by the methods and which
        contains volumes informations
        '''
        self.new_cell_key = int_cell
        self.new_surf_key = int_surf
        self.dictClassT4 = d_dictClassT4
        self.dictSurfaceT4 = d_dictSurfaceT4
        self.dicSurfaceMCNP = d_dicSurfaceMCNP
        self.dicCellMCNP = d_dicCellMCNP
        self.inputMCNP = CConfigParameters().readNameMCNPInputFile()

    def conversionEQUA(self, list_surface, fictive):
        '''
        :brief: method converting a list of if of surface and return a tuple with the
        informations of the volume EQUA T4
        '''

        str_equaMinus = ''
        str_equaPlus = ''
        i_minus = 0
        i_plus = 0
        seen = set()
        for elt in list_surface:
            if elt in seen:
                continue
            seen.add(elt)
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
        params = ['EQUA', str_equa]
        return params, s_fictive

    def conversionINTUNION(self, op, *ids, fictive):
        '''
        :brief: method analyze the type of conversion needed between a T4 INTERSECTION
        and a T4 UNION and return a tuple with the information of the T4 VOLUME
        '''
#         print('OP', op)
        params = []
        keyS = 100000
        if op == '*':
            params.extend(('EQUA', 'INTE'))
        if op == ':':
            tupleForEqua = self.conversionEQUA([keyS+1, -(keyS+2)], fictive=True)
            params.extend(tupleForEqua[0])
            params.append('UNION')
        params.append(len(ids))
        params.extend(ids)
        if fictive == False:
            s_fictive = ''
        if fictive == True:
            s_fictive = 'FICTIVE'
        tuple_final = params, s_fictive
#         print('tuple final',tuple_final)
        return tuple_final

    def postOrderTraversalFill(self, key, mcnp_new_dict,dictUniverse):

        if mcnp_new_dict[key].fillid is not None:
            new_cells = []
            cells_to_process = [] 
            mcnp_key_geom = mcnp_new_dict[key].geometry
            if mcnp_new_dict[key].costr:
#                 print('first fill tr', mcnp_new_dict[key].filltr)
                mcnp_new_dict[key].filltr[3:] = list(map(to_cos, mcnp_new_dict[key].filltr[3:]))
                mcnp_new_dict[key].costr = False
#                 print('second fill tr', mcnp_new_dict[key].filltr)
            mcnp_key_filltr = mcnp_new_dict[key].filltr
            for element in dictUniverse[int(mcnp_new_dict[key].fillid)]:
                cells_to_process.extend(self.postOrderTraversalFill(element, mcnp_new_dict,dictUniverse))
            for element in cells_to_process:
                mcnp_element_geom = mcnp_new_dict[element].geometry
                self.new_cell_key += 1
                new_key = self.new_cell_key
                mcnp_new_dict[new_key] = mcnp_new_dict[key].copy()
#                 print('new key cell',new_key, mcnp_new_dict[new_key].density)
                mcnp_new_dict[new_key].fillid = None
                mcnp_new_dict[new_key].materialID = mcnp_new_dict[element].materialID
                mcnp_new_dict[new_key].density = mcnp_new_dict[element].density
                mcnp_new_dict[new_key].idorigin = mcnp_new_dict[element].idorigin.copy()
                mcnp_new_dict[new_key].idorigin.append((element, key))
#                 print('idorigin', key, new_key, element, mcnp_new_dict[key].idorigin, mcnp_new_dict[new_key].idorigin)
#                 print('idorigin', id(mcnp_new_dict[key]), id(mcnp_new_dict[new_key]))
                tree = self.postOrderTraversalTransform(mcnp_element_geom, mcnp_key_filltr)
                mcnp_new_dict[new_key].geometry = ['*', mcnp_key_geom, tree]
                new_cells.append(new_key)
            return new_cells
        else:
            #mcnp_new_dict[key] = mcnp_new_dict[key].copy()
            return [key]


    def postOrderTraversalFlag(self, p_tree):
        '''
        :brief: method which take a tree and return a tuple of tuple with flag
        to decorate each tree in the tree
        '''

        if not isLeaf(p_tree):
            op, *args = p_tree
            new_args = [self.postOrderTraversalFlag(node) for node in args]
            self.new_cell_key += 1
            new_tree = [self.new_cell_key, op]
            new_tree.extend(new_args)
            return new_tree
        else:
            return p_tree

    def postOrderTraversalTransform(self, p_tree, p_transf):
        if isLeaf(p_tree):
#             print('PTREE',p_tree)
            surfaceObject = self.dicSurfaceMCNP[abs(p_tree)]
            if not p_transf:
                return p_tree
            p_boundCond = surfaceObject.boundaryCond
            p_typeSurface = surfaceObject.typeSurface
            l_paramSurface = surfaceObject.paramSurface
            idorigin = surfaceObject.idorigin + ['via tr']
            surfaceObject = CTransformationFonction().transformation(p_boundCond, p_transf, p_typeSurface, l_paramSurface, idorigin)
            surf_coll = CConversionSurfaceTransformed().conversion(surfaceObject)
            idorigin = surfaceObject.idorigin.copy()

            fixed_surfs = surf_coll.fixed
            fixed_ids = []
            for surf, side in fixed_surfs:
                self.new_surf_key += 1
                new_key = self.new_surf_key
                surf.idorigin.append('aux fixed surf')
                self.dictSurfaceT4[new_key] = (surf, [])
                fixed_ids.append(side * new_key)

            surf = surf_coll.main
            self.new_surf_key += 1
            new_key = self.new_surf_key
            self.dictSurfaceT4[new_key] = (surf, fixed_ids)
            self.dicSurfaceMCNP[new_key] = surfaceObject

            return new_key if p_tree >= 0 else -new_key
        else:
            op, *args = p_tree
            new_args = [self.postOrderTraversalTransform(node, p_transf) for node in args]
            new_tree = [op]
            new_tree.extend(new_args)
            return new_tree

    def postOrderTraversalConversion(self, p_tree, idorigin):
        '''
        :brief: method which take the tree create by m_postOrderTraversalFlag
        and filled a dictionary (of CVolumeT4 instance)
        '''
        if isLeaf(p_tree):
            self.new_cell_key += 1
            p_id = self.new_cell_key
            tupEQUA = self.conversionEQUA([p_tree], fictive=True)
            params, fict = tupEQUA
            self.dictClassT4[p_id] = CVolumeT4(params, fict, idorigin)
            return p_id

        p_id, op, *args = p_tree

        if op == '*':
            surfs = []
            nodes = []
            for arg in args:
                if isLeaf(arg):
                    surfs.append(arg)
                else:
                    nodes.append(arg)
            # here we know that paramsOPER starts as ['EQUA', 'INTE', ...]
            # because op == '*'
            if surfs:
                paramsEQUA, fict = self.conversionEQUA(surfs, fictive=True)
                params = paramsEQUA.copy()
                if nodes:
                    arg_ids = [self.postOrderTraversalConversion(node, idorigin)
                            for node in nodes]
                    paramsOPER, _fict = self.conversionINTUNION(op, *arg_ids, fictive=True)
                    params.extend(paramsOPER[1:])  # take everything after the EQUA
            else:
                # we assume that nodes is not empty
                arg_ids = [self.postOrderTraversalConversion(node, idorigin)
                        for node in nodes]
                paramsOPER, fict = self.conversionINTUNION(op, *arg_ids, fictive=True)
                params = paramsOPER.copy()  # take everything after the EQUA
            self.dictClassT4[p_id] = CVolumeT4(params, fict, idorigin)
            return p_id

        # here op == ':'
        if op != ':':
            raise ValueError('Converting cell with unexpected operator: %s'
                             % op)
        arg_ids = [self.postOrderTraversalConversion(arg, idorigin)
                    for arg in args]
        params, fict = self.conversionINTUNION(op, *arg_ids, fictive=True)
        self.dictClassT4[p_id] = CVolumeT4(params, fict, idorigin)
        return p_id


    def postOrderTraversalOptimisation(self, p_tree):
        '''
        :brief: method which permit to optimize the course of the cells MCNP
        '''

        if isLeaf(p_tree):
            return p_tree
        p_id, op, *args = p_tree
        new_args = [self.postOrderTraversalOptimisation(node) for node in args]
        new_node = [p_id, op]
        for node in new_args:
            if isIntersection(node) and op == '*':
                new_node.extend(node[2:])
            elif isUnion(node) and op == ':':
                new_node.extend(node[2:])
            else:
                new_node.append(node)
        return new_node

    def postOrderTraversalReplace(self, p_tree):
        if not isLeaf(p_tree):
            # print('replace: node {} is not a leaf'.format(p_tree))
            p_id, op, *args = p_tree
            new_tree = [p_id, op]
            new_tree.extend(self.postOrderTraversalReplace(node) for node in args)
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

        self.new_cell_key += 1
        if p_tree < 0:
            new_node = [self.new_cell_key, '*', p_tree]
            new_node.extend(Surface(surf) for surf in surfT4[1])
        else:
            new_node = [self.new_cell_key, ':', p_tree]
            new_node.extend(Surface(-surf) for surf in surfT4[1])
        #print('replace: replacing {} with {}'.format(p_tree, new_node))
        return GeomExpression(new_node)
    
    def postOrderTraversalCompl(self, tree):
#         print('TREE', tree)
        if not isinstance(tree, (list, tuple)):
            return tree
        if tree[0] == '^':
            geom = self.dicCellMCNP[int(tree[1])].geometry
#             print('GEOM', geom)
#             print('typegeom', type(geom))
            new_geom = self.postOrderTraversalCompl(geom)
#             print('NEW GEOM', new_geom)
            return new_geom.inverse()
#             if len(inverse) == 2:
#                 geombis = self.dicCellMCNP[int(inverse[0])].geometry
#                 inverse = geombis.inverse()
#             return GeomExpression(inverse)
        new_tree = [tree[0]]
        for node in tree[1:]:
            new_tree.append(self.postOrderTraversalCompl(node))
        result = GeomExpression(new_tree)
        return result
    
    def listSurfaceForLat(self, cellId):
        
        listeCouple = []   
        listSurface = extract_surfaces_list(self.dicCellMCNP[cellId].geometry)
        #check len(listeSurface) = 2,4,6
        while listSurface:
            surf = listSurface.pop(0)
            param = self.dicSurfaceMCNP[abs(surf)].paramSurface
            typeSurface = self.dicSurfaceMCNP[abs(surf)].typeSurface
            print('PARAM',surf, cellId, typeSurface, param)
            if isinstance(typeSurface, str):
                f = (param[0], param[1])
            else:
                _t, f, _s, _p = mcnp2cad[mcnp_to_mip(typeSurface)](param)
            #transformation
            normalVector = f[1]
            for i,surf2 in enumerate(listSurface):
                param2 = self.dicSurfaceMCNP[abs(surf2)].paramSurface
                typeSurface2 = self.dicSurfaceMCNP[abs(surf2)].typeSurface
                if isinstance(typeSurface2, str):
                    f2 = (param2[0], param2[1])
                else:
                    _t, f2, _s, _p = mcnp2cad[mcnp_to_mip(typeSurface2)](param2)
                point_final = (float(f2[0][0])-float(f[0][0]), float(f2[0][1])-float(f[0][1]), float(f2[0][2])-float(f[0][2]))
                distance = fabs(scal(point_final, normalVector))
                normalVector2 = f2[1]
                if fabs(scal(normalVector, normalVector2)) >= 0.99:
                    listeCouple.append(rescale(1./distance, normalVector))
                    break
            else:
                raise ValueError('No parallel surface found %d' %surf )
            listSurface.pop(i)
        return(listeCouple)
    
    def postOrderLattice(self, key, mcnp_new_dict):
        if mcnp_new_dict[key].lattice:
            domaine = CConfigParameters().readDomainForLattice(key)
            mcnp_element_geom = mcnp_new_dict[key].geometry
            list_info_surface = self.listSurfaceForLat(key)
            if len(list_info_surface) != len(domaine):
                raise ValueError('Problem of domain definition for lattice in cell %s; %d diff %d' %(key,len(list_info_surface),len(domaine)))
            vectors = self.latticeReciprocal(list_info_surface)
#             print('vectors', vectors, list(sqrt(scal(v, v)) for v in vectors))
            translations = self.latticeSpan(domaine, vectors, (0., 0., 0.))
            for transl in translations:
                tr = list(transl) + [1.,0.,0.,0.,1.,0.,0.,0.,1.]
#                 print('tr', tr)
                tree = self.postOrderTraversalTransform(mcnp_element_geom, tr)
                self.new_cell_key += 1
                new_key_cell = self.new_cell_key
                mcnp_new_dict[new_key_cell] = mcnp_new_dict[key].copy()
                mcnp_new_dict[new_key_cell].geometry = tree
                filltr = mcnp_new_dict[new_key_cell].filltr
                if filltr:
                    new_filltr = [x if i>2 else x+tr[i]
                                  for i,x in enumerate(filltr)]
                    mcnp_new_dict[new_key_cell].filltr = new_filltr
                else:
                    filltr = [0.,0.,0.,1.,0.,0.,0.,1.,0.,0.,0.,1.]
                    new_filltr = [x if i>2 else x+tr[i]
                                  for i,x in enumerate(filltr)]
                    mcnp_new_dict[new_key_cell].filltr = new_filltr
            del mcnp_new_dict[key]
            
    def latticeReciprocal(self, liste_info_surface):
        if len(liste_info_surface) == 1:
            return [rescale(1./scal(liste_info_surface[0], liste_info_surface[0]),liste_info_surface[0])]
        if len(liste_info_surface) == 2:
            a1,a2 = liste_info_surface
            a1_2=scal(a1, a1)
            a2_2 = scal(a2, a2)
            a1_a2 = scal(a1, a2)
            dem = a1_2*a2_2-a1_a2**2
            b1 = vsum(rescale(a2_2/dem, a1), rescale(-a1_a2/dem,a2))
            b2 = vsum(rescale(a1_2/dem, a2), rescale(-a1_a2/dem,a1))
            return [b1,b2]
        a1, a2, a3 = liste_info_surface
        dem = scal(a1, vect(a2, a3))
        b1 = rescale(1./dem, vect(a2, a3))
        b2 = rescale(1./dem, vect(a3, a1))
        b3 = rescale(1./dem, vect(a1, a2))
        return [b1,b2,b3]
            
            
    def latticeSpan(self, domaine, surfs, cur_transl):
        if not domaine:
            return [cur_transl]
        
        result = []
        interval = domaine[0]
        vector = surfs[0]
        for i in range(int(interval[0]),int(interval[1])+1):
            delta =  rescale(i, vector)
            transl = vsum(cur_transl, delta)
            result.extend(self.latticeSpan(domaine[1:], surfs[1:], transl))
        return result
                    
            
            
               
        

def scal(v1, v2):
    a1, b1, c1 = v1
    a2, b2, c2 = v2
    result = a1*a2 + b1*b2 + c1*c2
    return float(result)

def vect(v1,v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    result = (y1*z2-z1*y2,x2*z1-x1*z2,x1*y2-y1*x2)
    return result

def mixed(v1,v2,v3):
    return scal(v1, vect(v2, v3))

def rescale(a,v1):
    x1, y1, z1 = v1
    return (a*x1, a*y1, a*z1)

def vsum(v1,v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return (x1+x2, y1+y2, z1+z2)
# dic_test = dict()
# dic_cellT4 = dict()
# objT4 = CDictVolumeT4(dic_cellT4)
# for key, val in CDictCellMCNP().d_cellMCNP.items():
#     dic_test[key] = dict()
#     root = val.geometry
#     tree = root
#     obj_conversion = CCellConversion(key*1000, objT4)
#     tup = obj_conversion.postOrderTraversalFlag(tree)
#     opt_tree = obj_conversion.postOrderTraversalOptimisation(tup)
#     print('**********', opt_tree)
#     j = obj_conversion.postOrderTraversalConversion(opt_tree)
#     objT4.__setkey__(j, key)
#     objT4.__setitem__(key, objT4.__getitem__(j))
# for key, value in dic_cellT4.items():
#     print(key, dic_cellT4[key].operator, dic_cellT4[key].param)

#     if l != []:
#         tupEqua = CCellConversion(key*1000,objT4).conversionEQUA(l, fictive=True)
#         opT4, param, fict = tupEqua
#         print(i,tupEqua)
#         CCellConversion(key*1000,objT4).dictClassT4.__setitem__(i, CVolumeT4(opT4, param, fict))
# for key in dic_cellT4.keys():
#     print(key, dic_cellT4[key].operator, dic_cellT4[key].param)

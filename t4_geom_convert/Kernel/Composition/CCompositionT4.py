# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
:file : CCompositionT4.py
'''

class CCompositionT4:
    '''
    :brief: class which permits to objectify each element of the T4 file
    '''


    def __init__(self, p_typeDensity, p_material, p_valueOfDensity,
                 l_listMaterialComposition, nb_atom):
        '''
        Constructor
        '''
        self.typeDensity = p_typeDensity
        self.material = p_material
        self.valueOfDensity = p_valueOfDensity
        self.listMaterialComposition = l_listMaterialComposition
        self.nb_atom = nb_atom

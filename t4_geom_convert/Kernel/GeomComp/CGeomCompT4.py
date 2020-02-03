# -*- coding: utf-8 -*-
'''
Created on 7 févr. 2019

:author: Sogeti
:data : 07 february 2019
:file : CGeomCompT4.py
'''

class CGeomCompT4:
    '''
    :brief: Class of the object permitting to obtain information of the GeomComp
    of the T4 file
    '''

    def __init__(self, p_volumeNumberMaterial, l_listVolumeId):
        '''
        Constructor
        '''
        self.volumeNumberMaterial = p_volumeNumberMaterial
        self.listVolumeId = l_listVolumeId

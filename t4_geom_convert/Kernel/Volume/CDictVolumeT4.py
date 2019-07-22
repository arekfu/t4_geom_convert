# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CDictVolumeT4.py
'''

class CDictVolumeT4(object):
    '''
    :brief: Class inheriting of abstract class MutableMapping and
    listing volume for T4
    '''

    def __init__(self, dic_volumeT4):
        '''
        Constructor
        '''
        self.volumeT4 = dic_volumeT4

    def __getitem__(self, key):
        return self.volumeT4[key]

    def __setitem__(self, key, value):
        self.volumeT4[key] = value

    def set_key(self, key_old, key_new):
        self.volumeT4[key_old].id = key_new

    def __delitem__(self, key):
        del self.volumeT4[key]

    def __iter__(self):
        return iter(self.volumeT4)

    def __len__(self):
        return len(self.volumeT4)

    def __repr__(self):
        return self.volumeT4.__repr__()

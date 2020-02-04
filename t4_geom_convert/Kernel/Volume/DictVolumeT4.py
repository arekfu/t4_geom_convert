# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : DictVolumeT4.py
'''

from collections import OrderedDict
from collections.abc import MutableMapping


class DictVolumeT4(MutableMapping):
    '''A simple wrapper around an :class:`OrderedDict` for storing
    :class:`~.VolumeT4` objects.'''

    def __init__(self):
        '''Constructor'''
        self.dict_ = OrderedDict()

    def __getitem__(self, key):
        return self.dict_[key]

    def __setitem__(self, key, value):
        self.dict_[key] = value

    def replace_key(self, key_old, key_new):
        '''Replace the key of an element with the new key. This method also
        updates the ``id`` field of the :class:`VolumeT4` object associated to
        `key_old`.
        '''
        self.dict_[key_old].id = key_new
        self.dict_[key_new] = self.dict_[key_old]
        del self.dict_[key_old]

    def __delitem__(self, key):
        del self.dict_[key]

    def __iter__(self):
        return iter(self.dict_)

    def __len__(self):
        return len(self.dict_)

    def __repr__(self):
        return self.dict_.__repr__()

    def copy(self):
        '''Return a copy of `self`.'''
        new = DictVolumeT4()
        new.dict_ = self.dict_.copy()
        return new

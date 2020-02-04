# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : VolumeT4.py
'''


class VolumeT4:
    '''
    :brief: class which permits to access precisely of the value of a volume T4
    '''

    def __init__(self, pluses, minuses, ops=None, idorigin=None, fictive=True):
        '''
        Constructor
        '''
        self.pluses = set(pluses)
        self.minuses = set(minuses)
        self.ops = ops
        self.idorigin = idorigin.copy() if idorigin is not None else []
        self.fictive = fictive

    def __str__(self):
        str_params = ['EQUA']
        if self.pluses:
            str_params.extend(('PLUS', len(self.pluses)))
            str_params.extend(sorted(self.pluses))
        if self.minuses:
            str_params.extend(('MINUS', len(self.minuses)))
            str_params.extend(sorted(self.minuses))
        if self.ops is not None:
            str_params.extend((self.ops[0], len(self.ops[1])))
            str_params.extend(self.ops[1])
        if self.fictive:
            str_params.append('FICTIVE')
        return ' '.join(str(param) for param in str_params)

    def __repr__(self):
        return ('VolumeT4(pluses={}, minuses={}, ops={}, idorigin={}, '
                'fictive={})'.format(self.pluses, self.minuses, self.ops,
                                     self.idorigin, self.fictive))

    def comment(self):
        if self.idorigin:
            return ' // ' + '; '.join(map(str, self.idorigin))
        return ''

    def empty(self):
        '''Return `True` if the cell is patently empty, i.e. if the same
        surface ID appears with opposite signs.'''
        return bool(self.pluses & self.minuses)

    def surface_ids(self):
        '''Return the surface IDs used in this volume, as a set.'''
        return self.pluses | self.minuses

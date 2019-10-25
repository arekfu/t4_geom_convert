# -*- coding: utf-8 -*-
'''
Created on 5 févr. 2019

:author: Sogeti
:data : 05 february 2019
:file : CVolumeT4.py
'''


class CVolumeT4(object):
    '''
    :brief: class which permits to access precisely of the value of a volume T4
    '''

    def __init__(self, pluses, minuses, ops=None, idorigin=None, fictive=True):
        '''
        Constructor
        '''
        self.pluses = pluses.copy()
        self.minuses = minuses.copy()
        self.ops = ops.copy() if ops is not None else []
        self.idorigin = idorigin.copy() if idorigin is not None else []
        self.fictive = fictive

    def __str__(self):
        str_params = ['EQUA']
        if self.pluses:
            str_params.extend(('PLUS', len(self.pluses)))
            str_params.extend(self.pluses)
        if self.minuses:
            str_params.extend(('MINUS', len(self.minuses)))
            str_params.extend(self.minuses)
        for op, args in self.ops:
            str_params.extend((op, len(args)))
            str_params.extend(args)
        if self.fictive:
            str_params.append('FICTIVE')
        return ' '.join(str(param) for param in str_params)

    def __repr__(self):
        return ('CVolumeT4(pluses={}, minuses={}, ops={}, idorigin={}, '
                'fictive={})'.format(self.pluses, self.minuses, self.ops,
                                     self.idorigin, self.fictive))

    def comment(self):
        if self.idorigin:
            return ' // ' + '; '.join(map(str, self.idorigin))
        return ''

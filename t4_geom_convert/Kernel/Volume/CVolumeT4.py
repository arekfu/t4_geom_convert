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

    def __init__(self, p_operator, p_param, p_fictive, p_idorigin):
        '''
        Constructor
        '''
        self.operator = p_operator
        self.param = p_param
        self.fictive = p_fictive
        self.idorigin = p_idorigin

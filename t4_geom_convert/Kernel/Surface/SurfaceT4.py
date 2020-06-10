# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : SurfaceT4.py
'''

from itertools import chain


class SurfaceT4:
    '''Class that contains the information of the TRIPOLI-4 ``SURF``
    keyword.'''

    def __init__(self, type_surface, param_surface, idorigin=None):
        '''Constructor.

        :param type_surface: string specifying the type of the Surface
        :param param_surface: list of parameters describing the surface
        :param idorigin: a list of things that describe where this surface
            comes from
        '''

        self.type_surface = type_surface
        self.param_surface = tuple(param_surface)
        self.idorigin = idorigin if idorigin is not None else ()

    def __str__(self):
        as_str = ' '.join(str(element)
                          for element in chain((self.type_surface.name,),
                                               self.param_surface))
        return as_str

    def __repr__(self):
        return 'SurfaceT4({!r}, {!r}, {!r})'.format(self.type_surface,
                                                    self.param_surface,
                                                    self.idorigin)

    def comment(self):
        '''Return the comment string for this surface, if any.'''
        if self.idorigin:
            return ' // ' + '; '.join(map(str, self.idorigin))
        return ''

    def __eq__(self, other):
        # idorigin intentionally omitted
        return (self.type_surface == other.type_surface
                and self.param_surface == other.param_surface)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        # idorigin intentionally omitted
        return hash((self.type_surface, self.param_surface))

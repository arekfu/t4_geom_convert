# -*- coding: utf-8 -*-
'''Module containing the :class:`SurfaceCollection` class.'''


class SurfaceCollection:  # pylint: disable=too-few-public-methods
    '''A class that represents a single surface as a collection of surfaces.

    This class is necessary to represent, for instance, MCNP's macrobodies or
    one-nappe cones.
    '''
    def __init__(self, surfs):
        '''Instantiate a :class:`SurfaceCollection`.

        :param surfs: list of (surface, side) pairs
        '''
        if not surfs:
            raise ValueError('need a non-empty list of surfaces in '
                             'SurfaceCollection')
        self.surfs = sorted(surfs, key=lambda pair: -pair[1])
        if self.surfs[0][1] != 1:
            msg = ('At least one surface of the surface collection must be '
                   'oriented in the same way as the collection itself" {}'
                   .format(surfs))
            raise ValueError(msg) from None

    @classmethod
    def join(cls, surf_colls):
        '''Create a :class:`SurfaceCollection` from a list of pairs of
        :class:`SurfaceCollection` objects and integers.'''
        surfs = [(sub_surf, sub_side*side)
                 for surf_coll, side in surf_colls
                 for sub_surf, sub_side in surf_coll.surfs]
        return cls(surfs)

    def __repr__(self):
        return 'SurfaceCollection({!r})'.format(self.surfs)

'''Module containing the definition of the :class:`CollectionDict` class.'''

from collections.abc import MutableMapping

from MIP.geom.semantics import Surface


class CollectionDict(MutableMapping):
    '''This class represents a dictionary mapping MCNP surfaces (type
    :class:`~MIP.geom.semantics.Surface`) to lists of objects.

    For example, here we fill a dictionary with a couple of surfaces:

    >>> from MIP.geom.semantics import Surface
    >>> from t4_geom_convert.Kernel.Surface.SurfaceMCNP import SurfaceMCNP
    >>> import t4_geom_convert.Kernel.Surface.ESurfaceTypeMCNP as EMS
    >>> MS = EMS.ESurfaceTypeMCNP
    >>> planex = SurfaceMCNP('', MS.P, [1.0, 0.0, 0.0, 0.0], [])
    >>> planey = SurfaceMCNP('', MS.P, [0.0, 1.0, 0.0, 0.0], [])
    >>> planez = SurfaceMCNP('', MS.P, [0.0, 0.0, 1.0, 0.0], [])
    >>> dic = CollectionDict()
    >>> dic[1] = [(planex, 1)]
    >>> dic[Surface(2)] = [(planey, -1), (planez, 1)]

    In this example, surface 1 divides space in two regions (`x>0` and
    `x<0`), with the convention that `x>0` lies on the positive side of the
    surface.

    Surface 2 consists of two sub-surfaces (the `y=0` plane and the `z=0`
    plane). This again divides space in two regions: the first one, which by
    convention is the outer side of surface 2, lies on the negative side of
    `planey` and on the positive side of `planez` (i.e. it is the `y<0`, `z>0`
    quadrant); the other region is the complement of this quadrant, that is the
    union of `y>0` and `z<0`.

    You can query objects from the dictionary as usual:

    >>> dic[Surface(2)]
    [(SurfaceMCNP('', <ESurfaceTypeMCNP.P: 4>, (0.0, 1.0, 0.0, 0.0), (), ()), \
-1), (SurfaceMCNP('', <ESurfaceTypeMCNP.P: 4>, (0.0, 0.0, 1.0, 0.0), (), ()), \
1)]

    As you probably noticed above, you can also use integers in your queries:

    >>> dic[2] == dic[Surface(2)]
    True

    Finally, you can also query subsurfaces. Note that the numbering of the
    subsurfaces starts at 1 (MCNP convention):

    >>> dic[Surface(2, sub=1)]
    [(SurfaceMCNP('', <ESurfaceTypeMCNP.P: 4>, (0.0, 1.0, 0.0, 0.0), (), ()), \
-1)]
    >>> dic[Surface(2, sub=2)]
    [(SurfaceMCNP('', <ESurfaceTypeMCNP.P: 4>, (0.0, 0.0, 1.0, 0.0), (), ()), \
1)]

    Out-of-range subsurface indices are not allowed:
    >>> dic[Surface(2, sub=-1)]
    Traceback (most recent call last):
        ...
    IndexError: out of range subsurface (allowed range: [1, 2])

    You can also use two integers to query subsurfaces:
    >>> dic[2, 2] == dic[Surface(2, sub=2)]
    True

    You can modify subsurfaces, but you must always provide a list as a value:
    >>> dic[2, 2] = [(planex, -1)]
    >>> dic[2]
    [(SurfaceMCNP('', <ESurfaceTypeMCNP.P: 4>, (0.0, 1.0, 0.0, 0.0), (), ()), \
-1), (SurfaceMCNP('', <ESurfaceTypeMCNP.P: 4>, (1.0, 0.0, 0.0, 0.0), (), ()), \
-1)]
    '''

    def __init__(self):
        '''Initialize an empty dictionary.'''
        self.dic = {}

    def __getitem__(self, key):
        key = self._normalize_key(key)
        return self._get_item(*key)

    @staticmethod
    def _normalize_key(args):
        '''Normalize keys to a pair of integers (the second may be `None`).

        >>> from MIP.geom.semantics import Surface
        >>> CollectionDict._normalize_key(1)
        (1, None)
        >>> CollectionDict._normalize_key((1, 2))
        (1, 2)
        >>> CollectionDict._normalize_key(Surface(1))
        (1, None)
        >>> CollectionDict._normalize_key(Surface(1, 2))
        (1, 2)
        '''

        if isinstance(args, int):
            return (args, None)
        if isinstance(args, Surface):
            return (args.surface, args.sub)
        if not isinstance(args, tuple) or len(args) != 2:
            raise IndexError('expecting 1 int, 2 ints or a Surface as key in '
                             'CollectionDict, got {}'.format(args))
        if not isinstance(args[0], int) or not isinstance(args[1], int):
            raise TypeError('expecting int indices as keys in '
                            'CollectionDict')
        return args

    def _get_item(self, *key):
        '''Return the value of the item associated to `key`.

        :param key: the key to look up.
        :type key: (int, int or None)
        '''
        item = self.dic[key[0]]
        if key[1] is None:
            return item
        if key[1] <= 0 or key[1] > len(item):
            raise IndexError('out of range subsurface (allowed range: [1, {}])'
                             .format(len(item)))
        return [item[key[1]-1]]

    def __setitem__(self, key, value):
        key = self._normalize_key(key)
        self._set_item(*key, value=value)

    def _set_item(self, *key, value):
        '''Set the value of the item associated to `key`.

        :param key: the key to look up.
        :type key: (int, int or None)
        :param value: the value to set.
        :type value: list((SurfaceMCNP, int))
        '''
        if key[1] is None:
            self.dic[key[0]] = value
            return
        item = self.dic[key[0]]
        if key[1] <= 0 or key[1] > len(item):
            raise IndexError('out of range subsurface (allowed range: [1, {}])'
                             .format(len(item)))
        item[key[1]-1:key[1]] = value

    def __delitem__(self, item):
        del self.dic[item]

    def __iter__(self):
        yield from self.dic

    def __len__(self):
        return len(self.dic)

    def keys(self):
        yield from self.dic.keys()

    def values(self):
        yield from self.dic.values()

    def items(self):
        yield from self.dic.items()

    def number_items(self):
        '''Return a numbering of the items in the collection, as well as a
        matching between the keys in this dictionary and the keys in the
        numbering.'''
        numbering = {}
        matching = {}
        free_id = max(int(k) for k in self.dic) + 1
        for key, value in self.dic.items():
            first_surf, first_side = value[0]
            numbering[key] = first_surf
            ids = [first_side*key]
            for surf, side in value[1:]:
                numbering[free_id] = surf
                ids.append(side*free_id)
                free_id += 1
            matching[key] = ids
        return numbering, matching

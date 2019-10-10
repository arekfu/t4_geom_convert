'''Utilities for handling lattices.'''

from functools import reduce
from ..VectUtils import vsum, rescale, scal, vect


def latticeReciprocal(base_vecs):
    '''Yield the unit vectors of the reciprocal lattice.

    :param base_vecs: a list of one, two or three vectors describing the
                        base cell of the direct lattice. Vectors are triples
                        of the form ``(x, y, z)``.
    :returns: a list of one, two or three base vectors of the reciprocal
              lattice.

    >>> from math import isclose
    >>> from ..VectUtils import scal

    In the case of a one-dimensional lattice, the reciprocal vector has the
    same direction as the base vector, but its length is equal to the inverse
    of the length of the direct vector:
    >>> vec1 = (3, 0, 4)
    >>> rec1 = latticeReciprocal([vec1])[0]
    >>> isclose(scal(rec1, vec1), 1.0)
    True
    >>> isclose(scal(rec1, rec1) * scal(vec1, vec1), 1.0)
    True

    A few cases with two-dimensional lattices. The square lattice is self-dual:
    >>> vec1 = (1, 0, 0)
    >>> vec2 = (0, 1, 0)
    >>> latticeReciprocal([vec1, vec2])
    [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]

    A skew lattice:
    >>> vec1 = (1, 0, 0)
    >>> vec2 = (1, 1, 0)
    >>> latticeReciprocal([vec1, vec2])
    [(1.0, -1.0, 0.0), (0.0, 1.0, 0.0)]

    In three dimensions, the cubic lattice is self-dual:
    >>> vec1 = (1, 0, 0)
    >>> vec2 = (0, 1, 0)
    >>> vec3 = (0, 0, 1)
    >>> latticeReciprocal([vec1, vec2, vec3])
    [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]

    The length of the reciprocal vectors are inversely proportional to the
    length of the base vectors of the direct lattice:
    >>> vec1 = (2, 0, 0)
    >>> vec2 = (0, 4, 0)
    >>> vec3 = (0, 0, 0.5)
    >>> latticeReciprocal([vec1, vec2, vec3])
    [(0.5, 0.0, 0.0), (0.0, 0.25, 0.0), (0.0, 0.0, 2.0)]
    '''

    if len(base_vecs) == 1:
        unit = rescale(1./scal(base_vecs[0], base_vecs[0]), base_vecs[0])
        return [unit]
    if len(base_vecs) == 2:
        vec1, vec2 = base_vecs
        vec12 = scal(vec1, vec1)
        vec22 = scal(vec2, vec2)
        vec1_vec2 = scal(vec1, vec2)
        den = vec12*vec22 - vec1_vec2**2
        rec1 = vsum(rescale(vec22/den, vec1), rescale(-vec1_vec2/den, vec2))
        rec2 = vsum(rescale(vec12/den, vec2), rescale(-vec1_vec2/den, vec1))
        return [rec1, rec2]
    vec1, vec2, vec3 = base_vecs
    vec12 = vect(vec1, vec2)
    vec23 = vect(vec2, vec3)
    vec31 = vect(vec3, vec1)
    norm = 3. / (scal(vec1, vec23) + scal(vec2, vec31) + scal(vec3, vec12))
    rec1 = rescale(norm, vec23)
    rec2 = rescale(norm, vec31)
    rec3 = rescale(norm, vec12)
    return [rec1, rec2, rec3]


def latticeVector(base_vecs, index):
    '''Compute a lattice displacement vector from a set of basis vectors and a
    tuple of indices.

    >>> base_vecs = [(1, 0, 0),
    ...              (0, 0, 2)]
    >>> latticeVector(base_vecs, (0, 0))
    (0.0, 0.0, 0.0)
    >>> latticeVector(base_vecs, (3, 2))
    (3.0, 0.0, 4.0)
    >>> latticeVector(base_vecs, (-1, -1))
    (-1.0, 0.0, -2.0)
    '''
    return vsum(*(rescale(float(i), vec) for i, vec in zip(index, base_vecs)))


class LatticeBounds:
    '''A simple class to hold a list of range bounds. It provides some useful
    services such as the :meth:`~.size` method.
    '''
    def __init__(self, bounds):
        if not isinstance(bounds, list):
            raise TypeError('Expected a list of pairs of integers')
        for elem in bounds:
            if (not isinstance(elem, tuple) or len(elem) != 2
                    or not isinstance(elem[0], int)
                    or not isinstance(elem[1], int)):
                raise TypeError('Expected a list of pairs of integers')
        self.bounds = bounds.copy()

    def size(self):
        '''Return the total size of the range bounds, i.e. the product of the
        range lengths.

        >>> LatticeBounds([(0, 4)]).size()
        5
        >>> LatticeBounds([(-1, 1), (-3, 3)]).size()
        21
        >>> LatticeBounds([]).size()
        1
        '''
        return reduce(lambda x, y: x * (y[1] - y[0] + 1), self.bounds, 1)

    def __len__(self):
        '''Return the number of dimensions.'''
        return len(self.bounds)

    def __iter__(self):
        yield from self.bounds

    def __repr__(self):
        return repr(self.bounds)

    def __eq__(self, other):
        if isinstance(other, list):
            return self.bounds == other
        if isinstance(other, LatticeBounds):
            return self.bounds == other.bounds
        return False

    def copy(self):
        '''Return a copy of `self`.'''
        return LatticeBounds(self.bounds.copy())

    def indices(self):
        '''Yield all the valid indices in the bounds, in canonical order (loop
        over the leftmost index first).

        >>> bounds = LatticeBounds([(-1, 1), (-2, 2)])
        >>> list(bounds.indices())
        [(-1, -2), (0, -2), (1, -2), (-1, -1), (0, -1), (1, -1), (-1, 0), \
(0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
        >>> list(LatticeBounds([(0, 2)]).indices())
        [(0,), (1,), (2,)]
        '''
        def _indices(bounds):
            if len(bounds) == 1:
                bounds0 = bounds[0]
                yield from ([x] for x in range(bounds0[0], bounds0[1] + 1))
            else:
                tail = bounds[-1]
                rest = bounds[:-1]
                for elem in range(tail[0], tail[1] + 1):
                    for heads in _indices(rest):
                        yield heads + [elem]
        yield from map(tuple, _indices(self.bounds))


def parse_ranges(intervals):
    '''Parse a list of intervals (in the MCNP syntax: ``start:end``) into a
    list of pairs of integers.

    :param intervals: A list of strings of the form :samp:`'{i}:{j}'`, where
                      `i` and `j` are integers.
    :type intervals: list(str)
    :returns: a list of pairs of integers representing the parsed bounds
    :rtype: list((int,int))

    >>> parse_ranges(['0:4', '0:4', '0:4'])
    [(0, 4), (0, 4), (0, 4)]
    >>> parse_ranges(['1:2', '3:4', '5:6', '7:8'])
    [(1, 2), (3, 4), (5, 6), (7, 8)]
    >>> parse_ranges([])
    []
    >>> parse_ranges(['0::5'])
    Traceback (most recent call last):
        ...
    ValueError: needs exactly 2 colon-separated range bounds in argument '0::5'
    '''
    bounds_list = []
    for rang in intervals:
        bounds = rang.split(':')
        if len(bounds) != 2:
            raise ValueError('needs exactly 2 colon-separated range '
                             'bounds in argument {!r}'
                             .format(rang))
        try:
            start = int(bounds[0])
        except ValueError:
            raise ValueError('range bound {!r} is not an integer'
                             .format(bounds[0])) from None
        try:
            end = int(bounds[1])
        except ValueError:
            raise ValueError('range bound {!r} is not an integer'
                             .format(bounds[1])) from None
        bounds_list.append((start, end))
    return LatticeBounds(bounds_list)


class LatticeSpec:
    '''A simple class that holds a list of `n*m*l` integers and provides
    n-dimensional indexing into the list.
    '''
    def __init__(self, bounds, spec):
        if not isinstance(bounds, LatticeBounds):
            raise TypeError('Expected a LatticeBounds object for the `bounds` '
                            'argument')
        if not isinstance(spec, (list, tuple)):
            raise TypeError('Expected a list or a tuple for the `spec` '
                            'argument')
        if bounds.size() != len(spec):
            raise ValueError('The `spec` argument must have exactly {} '
                             'elements'.format(bounds.size()))
        self.bounds = bounds.copy()
        self.spec = spec

    def __getitem__(self, arg):
        '''Index into the lattice bounds.

        >>> bounds = LatticeBounds([(1, 4), (0, 1)])
        >>> spec = LatticeSpec(bounds, list(range(8)))

        Sequential indexing is supported:
        >>> spec[0]
        0
        >>> spec[2]
        2

        Indexing by a tuple of indices assumes that the first index represents
        the inner loop:
        >>> spec[1, 0]
        0
        >>> spec[1, 1]
        1
        >>> spec[4, 1]
        7

        It works with tuples, too:
        >>> spec = LatticeSpec(bounds, tuple(range(8)))
        >>> spec[0]
        0
        >>> spec[1, 1]
        1
        '''
        if isinstance(arg, tuple):
            if len(arg) != len(self.bounds):
                raise ValueError('Expected a tuple of {} elements'
                                 .format(len(self.bounds)))
            index = 0
            for bound, subind in zip(self.bounds, arg):
                if subind < bound[0] or subind > bound[1]:
                    raise ValueError('index {} out of bounds ({}, {})'
                                     .format(subind, bound[0], bound[1]))
                index = index * (bound[1] - bound[0] + 1) + subind - bound[0]
        elif isinstance(arg, int):
            index = arg
        else:
            raise TypeError('LatticeSpec can only be indexed with a tuple or '
                            'an integer')
        return self.spec[index]

    def __repr__(self):
        return 'LatticeSpec({}, {})'.format(self.bounds, self.spec)

    def __iter__(self):
        yield from self.spec

    def items(self):
        '''Iterate over the lattice indices and the lattice specification, as
        `(indices, spec)` pairs.

        >>> bounds = LatticeBounds([(1, 2), (0, 1)])
        >>> spec = LatticeSpec(bounds, ['a', 'b', 'c', 'd'])
        >>> list(spec.items())
        [((1, 0), 'a'), ((2, 0), 'b'), ((1, 1), 'c'), ((2, 1), 'd')]
        '''
        yield from zip(self.bounds.indices(), self.spec)

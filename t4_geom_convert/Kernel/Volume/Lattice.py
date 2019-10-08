'''Utilities for handling lattices.'''

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
        vec1_2 = scal(vec1, vec1)
        vec2_2 = scal(vec2, vec2)
        vec1_vec2 = scal(vec1, vec2)
        den = vec1_2*vec2_2 - vec1_vec2**2
        rec1 = vsum(rescale(vec2_2/den, vec1), rescale(-vec1_vec2/den, vec2))
        rec2 = vsum(rescale(vec1_2/den, vec2), rescale(-vec1_vec2/den, vec1))
        return [rec1, rec2]
    vec1, vec2, vec3 = base_vecs
    vec12 = vect(vec1, vec2)
    vec23 = vect(vec2, vec3)
    vec31 = vect(vec3, vec1)
    det = (scal(vec1, vec23) + scal(vec2, vec31) + scal(vec3, vec12)) / 3.
    norm = 1./ det
    rec1 = rescale(norm, vec23)
    rec2 = rescale(norm, vec31)
    rec3 = rescale(norm, vec12)
    return [rec1, rec2, rec3]


def latticeVectors(base_vecs, indices):
    '''Generate lattice vectors from a set of basis vectors and a list of
    indices.

    >>> base_vecs = [(1, 0, 0),
    ...              (0, 0, 2)]
    >>> list(latticeVectors(base_vecs, [(0, 0), (3, 2), (-1, -1)]))
    [(0.0, 0.0, 0.0), (3.0, 0.0, 4.0), (-1.0, 0.0, -2.0)]
    '''
    for ind in indices:
        yield vsum(*(rescale(float(i), vec) for i, vec in zip(ind, base_vecs)))


def latticeIndices(domain):
    '''Generate all the valid indices in the given domain.

    :param domain: A list of pairs representing (inclusive) index bounds
    :type domain: list(tuple(int))
    :returns: the indices, as tuples

    >>> bounds = [(4, 8)]
    >>> list(latticeIndices(bounds))
    [[4], [5], [6], [7], [8]]
    >>> bounds = [(0, 2), (-1, 1)]
    >>> list(latticeIndices(bounds))
    [[0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1], [2, -1], [2, 0], [2, 1]]
    >>> bounds = [(0, 1), (0, 1), (0, 1)]
    >>> list(latticeIndices(bounds))
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], \
[1, 1, 0], [1, 1, 1]]
    '''
    def _latticeIndicesRec(domain, cur_indices):
        if not domain:
            yield cur_indices
            return
        interval = domain[0]
        for i in range(int(interval[0]), int(interval[1])+1):
            new_indices = cur_indices + [i]
            yield from _latticeIndicesRec(domain[1:], new_indices)

    yield from _latticeIndicesRec(domain, [])


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
    return bounds_list

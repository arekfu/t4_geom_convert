'''Utilities for handling lattices.'''

from functools import reduce
from ..VectUtils import (vsum, vdiff, rescale, scal, vect, mag2,
                         pointInPlaneIntersection, planeSide,
                         projectPointOnPlane)


class LatticeError(Exception):
    '''An exception class for errors generated during lattice processing.'''


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
        vec12 = mag2(vec1)
        vec22 = mag2(vec2)
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

    def __getitem__(self, i):
        '''Return the i-th element in the list of range bounds.

        >>> LatticeBounds([(-1, 1), (-3, 3)])[1]
        (-3, 3)
        >>> LatticeBounds([(-1, 1), (-3, 3)])[4]
        Traceback (most recent call last):
            ...
        IndexError: list index out of range
        '''
        return self.bounds[i]

    def __len__(self):
        '''Return the number of dimensions.'''
        return len(self.bounds)

    def dims(self):
        '''Return the number of non-trivial dimensions.'''
        return sum(1 for x in self.bounds if x[0] != x[1])

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
                            'argument, got a {}'.format(type(bounds)))
        if not isinstance(spec, (list, tuple)):
            raise TypeError('Expected a list or a tuple for the `spec` '
                            'argument, got a {}'.format(type(spec)))
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


def squareLatticeReciprocalVecs(surfaces):
    '''Compute the reciprocal vectors of a square lattice.'''
    if len(surfaces) not in (2, 4, 6):
        raise LatticeError('Lattice base cell has {} surfaces; 2, 4 or 6 '
                           'were expected'.format(len(surfaces)))

    base_vecs = []
    while surfaces:
        (surf_1, side_1), (surf_2, _) = surfaces[0:2]
        point, normal = surf_1
        if side_1 == 1:
            normal = rescale(-1, normal)
        point2, _normal2 = surf_2
        point_diff = vdiff(point, point2)
        distance = scal(point_diff, normal)
        base_vecs.append(rescale(1./distance, normal))
        surfaces = surfaces[2:]
    return base_vecs


def squareLatticeBaseVectors(surfaces):
    '''Compute the base vectors of a square lattice.'''
    lat_rec_vectors = squareLatticeReciprocalVecs(surfaces)
    return latticeReciprocal(lat_rec_vectors)


def hexLatticeBaseVectors(surfaces):
    '''Compute the base vectors for a hexagonal lattice.'''
    vertices_0, axis = hexVertices(surfaces, 0)
    vertices_2, _ = hexVertices(surfaces, 2)
    base_vecs = [vdiff(vertices_0[0], vertices_0[2]),
                 vdiff(vertices_2[0], vertices_2[2])]
    if len(surfaces) == 8:
        # the base cell has axial bounds
        bottom_pt = projectPointOnPlane(vertices_0[0], surfaces[-1][0], axis)
        top_pt = projectPointOnPlane(vertices_0[0], surfaces[-2][0], axis)
        base_vecs.append(vdiff(top_pt, bottom_pt))
    return base_vecs


def hexVertices(surfs, first_side):
    '''Return the vertices of a base of the hexagonal prism described by the
    given surfaces and the direction of the prism axis.

    The vertices are returned as a list of points. This function guarantees
    that the returned vertices are consecutive (i.e. ``v[i]`` and ``v[i+i]``
    share a side, and so do ``v[-1]`` and ``v[0]``).

    The `first_side` argument is an integer from 0 to 5 that specifies which
    side should be shared by ``v[0]`` and ``v[-1]``.

    The prism axis is returned as a vector.

    Example:

    >>> vertices = [(0, 1, 0), (3, 1, 0), (5, 2, 0),
    ...             (5, 3, 0), (2, 3, 0), (0, 2, 0)]
    >>> sides = [vdiff(v2, v1)
    ...          for v1, v2 in zip(vertices, vertices[1:] + [vertices[0]])]
    >>> from t4_geom_convert.Kernel.VectUtils import renorm, vect
    >>> normals = [renorm(vect(side, (0, 0, 1))) for side in sides]
    >>> planes = [((vertices[i], normals[i]), -1)  # -1 is the side
    ...           for i in (3, 0, 1, 4, 2, 5)]

    This is the same weird hexagonal prism that is used in the docstring for
    :func:`hexSortSides`.

    Calling :func:`hexVertices` with ``first_side=0`` yields the vertices of
    the hexagon sorted in such a way that the first one and the last one lie on
    side 0:

    >>> verts, axis = hexVertices(planes, 0)
    >>> from t4_geom_convert.Kernel.VectUtils import isPointOnPlane
    >>> isPointOnPlane(verts[0], planes[0][0])
    True
    >>> isPointOnPlane(verts[-1], planes[0][0])
    True

    Other values of `first_side` lead to different orderings of the vertices:

    >>> verts, axis = hexVertices(planes, 4)
    >>> isPointOnPlane(verts[0], planes[4][0])
    True
    >>> isPointOnPlane(verts[-1], planes[4][0])
    True

    We can check that each plane contains exactly two vertices:

    >>> [sum(1 for vert in verts if isPointOnPlane(vert, plane[0]))
    ...  for plane in planes]
    [2, 2, 2, 2, 2, 2]

    The `axis` vector, by construction is parallel to all the side planes:

    >>> from t4_geom_convert.Kernel.VectUtils import isVectorParallelToPlane
    >>> all(isVectorParallelToPlane(axis, plane[0]) for plane in planes)
    True

    It is also possible to pass a list of eight planes. In this case, the
    hexagon is guaranteed to lie on the "top" plane (i.e. `surfs[-2]`).

    >>> planes += [(((10.0, 0.0, 0.0), (1.0, 1.0, 1.0)), -1),
    ...            (((-10.0, 0.0, 0.0), (1.0, 1.0, 1.0)), 1)]
    >>> verts, axis = hexVertices(planes, 2)
    >>> all(isPointOnPlane(vert, planes[-2][0]) for vert in verts)
    True
    >>> [sum(1 for vert in verts if isPointOnPlane(vert, plane[0]))
    ...  for plane in planes[:-2]]
    [2, 2, 2, 2, 2, 2]
    >>> all(isVectorParallelToPlane(axis, plane[0]) for plane in planes[:-2])
    True
    '''
    assert len(surfs) in (6, 8)
    assert 0 <= first_side < 6
    adj = hexSortSides(surfs[:6])
    prism_dir = next(inters[1] for inters in adj.values()
                     if inters is not None)
    if len(surfs) == 6:
        top_plane = ((0.0, 0.0, 0.0), prism_dir)
    else:  # 8 planes
        top_plane = surfs[-2][0]
    vertices = []
    seen = {first_side}
    cur_ind = first_side
    while len(vertices) < 6:
        if len(seen) == 6:
            seen.remove(first_side)
        for i in range(6):
            if i in seen:
                continue
            inters = adj[tuple(sorted([cur_ind, i]))]
            if inters is not None:
                proj_pt = projectPointOnPlane(inters[0], top_plane, inters[1])
                vertices.append(proj_pt)
                cur_ind = i
                seen.add(i)
                break
    return vertices, prism_dir


def hexSortSides(surfs):
    r'''Return an adjacency dictionary for the sides of the hexagon. The
    dictionary keys are pairs of indices of sides of the hexagon; the possible
    values are `None` if the given sides are not adjacent, or a straight line
    (in `(point, direction)` form) representing the intersection between the
    two planes if they are adjacent. The keys are always sorted in such a way
    that the smallest index comes first: so, for instance, `(0, 1)` is a
    possible key, but `(1, 0)` is not.

    The `surfs` argument is the list of surfaces representing the hexagon. Each
    surface must be a `(plane, side)` pair, where `plane` is a plane
    (represented as a `(point, normal)` pair) and `side` indicates on which
    side of the plane the hexagonal cell lies (±1). The surfaces in `surfs`
    must appear in the canonical order: first, the surface that separates the
    base cell of the hexagonal lattice from the `(1, 0, 0)` cell; then the
    opposite plane; then the surface that separates the base cell from the `(0,
    1, 0)` cell; then the opposite plane; and, finally, the two remaining
    planes, in no particular order.

    As an example, consider the regular hexagon:

    >>> from math import cos, sin, pi, isclose, fabs
    >>> vertices = [(cos(i*pi/3.), sin(i*pi/3.), 0.) for i in range(6)]
    >>> sides = [vdiff(v2, v1)
    ...          for v1, v2 in zip(vertices, vertices[1:] + [vertices[0]])]

    We compute the normals to the planes:

    >>> from t4_geom_convert.Kernel.VectUtils import renorm, vect
    >>> normals = [renorm(vect(side, (0, 0, 1))) for side in sides]
    ... # these are outgoing normals

    The hexagon looks like this:

                      2
                  ---------
                 /         \
             4  /           \ 0
               /             \
               \             /
             1  \           / 5
                 \         /
                  ---------
                      3

    The numbers indicate the way we have chosen to order the planes. We
    construct the list of surfaces to respect this constraint:

    >>> planes = [((vertices[i], normals[i]), -1)  # -1 is the side
    ...           for i in (0, 3, 1, 4, 2, 5)]

    Here is the adjacency dictionary:

    >>> adj = hexSortSides(planes)
    >>> adj[(0, 2)] is not None
    True
    >>> adj[(0, 5)] is not None
    True
    >>> adj[(0, 1)] is None
    True

    We can also modify the plane numbering. For instance:

                      5
                  ---------
                 /         \
             2  /           \ 0
               /             \
               \             /
             1  \           / 3
                 \         /
                  ---------
                      4

    >>> planes = [((vertices[i], normals[i]), -1)  # -1 is the side
    ...           for i in (0, 3, 2, 5, 4, 1)]
    >>> adj = hexSortSides(planes)
    >>> adj[(0, 2)] is None
    True
    >>> adj[(0, 3)] is not None
    True
    >>> point, direction = adj[(0, 3)]
    >>> (isclose(point[0], 1)
    ...  and isclose(point[1], 0, abs_tol=1e-10)
    ...  and isclose(point[2], 0, abs_tol=1e-10))
    True
    >>> (isclose(direction[0], 0, abs_tol=1e-10)
    ...  and isclose(direction[1], 0, abs_tol=1e-10)
    ...  and isclose(fabs(direction[2]), 1))
    True

    We can also test a weird hexagon:

    >>> vertices = [(0, 1, 0), (3, 1, 0), (5, 2, 0),
    ...             (5, 3, 0), (2, 3, 0), (0, 2, 0)]
    >>> sides = [vdiff(v2, v1)
    ...          for v1, v2 in zip(vertices, vertices[1:] + [vertices[0]])]
    >>> normals = [renorm(vect(side, (0, 0, 1))) for side in sides]

    It looks approximately like this:

                0
           /---------+
        3 /          |
         /           | 4
        |           /
      5 |          / 2
        *---------/
             1

    The star represents the first vertex and the sides unfold counterclockwise.
    We impose the numbering given in the figure:

    >>> planes = [((vertices[i], normals[i]), -1)  # -1 is the side
    ...           for i in (3, 0, 1, 4, 2, 5)]
    >>> adj = hexSortSides(planes)
    >>> adj[(0, 1)] is None
    True
    >>> adj[(0, 2)] is None
    True
    >>> adj[(0, 3)] is not None
    True
    >>> point, _ = adj[(0, 3)]
    >>> point
    (2.0, 3.0, 0.0)
    >>> point, _ = adj[(1, 2)]
    >>> point
    (3.0, 1.0, 0.0)
    '''
    if len(surfs) != 6:
        raise LatticeError('hexSortSides() must be called with 6 planes')

    adjacency = {}
    for i in range(6):
        for j in range(i+1, 6):
            if i // 2 == j // 2:
                adjacency[(i, j)] = None
                continue
            other_group = (i // 2 + j // 2) * 2 % 3
            k1 = 2*other_group  # pylint: disable=invalid-name
            k2 = k1 + 1         # pylint: disable=invalid-name
            inters = areHexSidesAdjacent(surfs[i][0], surfs[j][0],
                                         surfs[k1], surfs[k2])
            adjacency[(i, j)] = inters
    n_inters = sum(1 for inters in adjacency.values() if inters is not None)
    if n_inters != 6:
        msg = ('not enough intersections ({}) between the planes of the '
               'hexagonal base cell:\nadj: {}'.format(n_inters, adjacency))
        raise LatticeError(msg)
    return adjacency


def areHexSidesAdjacent(plane1, plane2, other_surf1, other_surf2):
    '''If `plane1` and `plane2` are adjacent in the hexagonal prism closed off
    by `other_plane1` and `other_plane2`, this function returns the line given
    by the intersection of the two planes, in the form of a `(point, vector)`
    pair; otherwise, it returns `None`.'''
    other_plane1, side1 = other_surf1
    other_plane2, side2 = other_surf2
    int_pt, line_vec = pointInPlaneIntersection(plane1, plane2)
    actual_side1 = planeSide(int_pt, other_plane1)
    actual_side2 = planeSide(int_pt, other_plane2)
    if side1 == actual_side1 and side2 == actual_side2:
        return int_pt, line_vec
    return None

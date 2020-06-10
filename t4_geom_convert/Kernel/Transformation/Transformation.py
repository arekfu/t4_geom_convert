# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
'''

from math import sqrt
from collections import OrderedDict
import numpy as np

from MIP.geom.forcad import transform_frame
from MIP.geom.transforms import get_transforms

from ..Surface.SurfaceMCNP import SurfaceMCNP
from .TransformationQuad import transformation_quad
from .TransformationError import TransformationError

from ..Surface.ESurfaceTypeMCNP import ESurfaceTypeMCNP as MS
from ..VectUtils import transpose, matrix_rows, scal, renorm, vdiff, vect


def get_mcnp_transforms(parser):
    '''Return the dictionary of parsed MCNP transformation, in a canonical,
    12-parameter form.

    :param parser: the MCNP parser
    :returns: a dictionary associating each transformation number to a list of
        12 transformation parameters.
    '''
    mcnp_transforms = get_transforms(parser)
    transforms = OrderedDict()
    for transf_id, transf in mcnp_transforms.items():
        try:
            transf = normalize_transform(transf)
        except TransformationError as err:
            raise TransformationError('{}\nThe problematic transformation '
                                      'was TR{}={}'
                                      .format(err, transf_id, transf))
        transforms[transf_id] = transf
    return transforms


def normalize_transform(transf):
    '''Return a normalized, 12-param version of the affine transformation.
    '''
    if len(transf) == 13 and transf[-1] != 1:
        raise TransformationError('Transformations with m=-1 are not supported'
                                  ' yet.')
    return transf[:3] + normalize_matrix(transf[3:12])


def normalize_matrix(matrix):
    '''Return a normalized version of the given 3x3 rotation matrix.

    The input matrix may be missing some elements (3, 5, 6 and 9 elements are
    possible) or some of the elements may be `None`. The rules for normalizing
    a 3x3 rotation matrix are given in the MCNP6 manual, section 3.3.1.3 (TR
    card, Surface coordinate transformation).
    '''
    identity = [1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0]
    # normalize the list so that it always contains 9 elements
    matrix9 = matrix + [None] * (9 - len(matrix))
    n_values = sum(1 for elem in matrix9 if elem is not None)
    if n_values == 9: # easy
        return matrix
    if n_values == 0: # easy
        return identity
    if n_values == 5:
        return normalize_matrix5(matrix9)

    # did the user define whole rows?
    rows_given = is_matrix_rowwise(matrix9)

    if n_values == 3:
        if rows_given:
            return normalize_matrix3(matrix9)
        return transpose(normalize_matrix3(transpose(matrix9)))
    if n_values == 6:
        # two rows or two columns, determine the third by cross-product
        if rows_given:
            return normalize_matrix6(matrix9)
        # two columns were defined; transpose, normalize and transpose back
        return transpose(normalize_matrix6(transpose(matrix9)))
    raise TransformationError('Malformed matrix {} has {} non-None elements; '
                              '0, 3, 5, 6 or 9 elements are expected'
                              .format(matrix, n_values))


def is_matrix_rowwise(matrix):
    '''Returns `True` if the matrix has at least one fully defined row.

    >>> is_matrix_rowwise([1, 2, 3, 4, 5, 6, 7, 8, 9])
    True
    >>> is_matrix_rowwise([None, None, None, 4, 5, 6, 7, 8, 9])
    True
    >>> is_matrix_rowwise([1, 2, 3, None, None, None, 7, 8, 9])
    True
    >>> is_matrix_rowwise([1, 2, 3, 4, 5, 6, None, None, None])
    True
    >>> is_matrix_rowwise([None, 2, 3, None, 5, 6, None, 8, 9])
    False
    >>> is_matrix_rowwise([1, None, 3, 4, None, 6, 7, None, 9])
    False
    >>> is_matrix_rowwise([1, 2, None, 4, 5, None, 7, 8, None])
    False
    >>> is_matrix_rowwise([None, None, None, None, None, None, 7, 8, 9])
    True
    >>> is_matrix_rowwise([None, None, None, 4, 5, 6, None, None, None])
    True
    >>> is_matrix_rowwise([1, 2, 3, None, None, None, None, None, None])
    True
    >>> is_matrix_rowwise([None, None, 3, None, None, 6, None, None, 9])
    False
    >>> is_matrix_rowwise([1, None, None, 4, None, None, 7, None, None])
    False
    >>> is_matrix_rowwise([None, 2, None, None, 5, None, None, 8, None])
    False
    '''
    a_row = matrix[0:3]
    return (all(elem is not None for elem in a_row)
            or all(elem is None for elem in a_row))


def normalize_matrix3(matrix):
    '''Return the canonical form of a 3x3 matrix where exactly one row has been
    defined.

    >>> from ..VectUtils import scal, rotate
    >>> mat = normalize_matrix3([1.0, 0.0, 0.0,
    ...                          None, None, None,
    ...                          None, None, None])
    >>> rows = matrix_rows(mat)
    >>> rows[0] == [1, 0, 0]
    True
    >>> scal(rows[0], rows[1])
    0.0
    >>> scal(rows[0], rows[2])
    0.0
    >>> scal(rows[1], rows[2])
    0.0
    >>> scal(rows[0], rows[0])
    1.0
    >>> scal(rows[1], rows[1])
    1.0
    >>> scal(rows[2], rows[2])
    1.0

    We can also check that it works with a somewhat generically aligned vector:

    >>> vec = rotate((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 37.5)
    >>> vec = rotate(vec, (0.0, 0.0, 1.0), 194.2)
    >>> vec = rotate(vec, (1.0, 0.0, 0.0), -446.3)
    >>> mat = normalize_matrix3([None]*3 + list(vec) + [None]*3)
    >>> rows = matrix_rows(mat)
    >>> rows[1] == list(vec)
    True
    >>> abs(scal(rows[0], rows[1])) < 1e-10
    True
    >>> abs(scal(rows[0], rows[2])) < 1e-10
    True
    >>> abs(scal(rows[1], rows[2])) < 1e-10
    True
    >>> abs(scal(rows[0], rows[0]) - 1.0) < 1e-10
    True
    >>> abs(scal(rows[1], rows[1]) - 1.0) < 1e-10
    True
    >>> abs(scal(rows[2], rows[2]) - 1.0) < 1e-10
    True
    '''
    rows = matrix_rows(matrix)
    i_row1 = next(i for i, row in enumerate(rows) if row[0] is not None)
    i_row2 = (i_row1 + 1) % 3
    i_row3 = (i_row2 + 1) % 3
    row1 = rows[i_row1]
    ex = (1.0, 0.0, 0.0)
    ey = (0.0, 1.0, 0.0)
    e2 = ey if scal(row1, ex) > 0.999 else ex
    row2 = renorm(vdiff(e2, renorm(row1, norm=scal(e2, row1))))
    row3 = vect(row1, row2)
    norm_matrix = matrix.copy()
    norm_matrix[3*i_row2:3*i_row2 + 3] = row2
    norm_matrix[3*i_row3:3*i_row3 + 3] = row3
    return norm_matrix


def normalize_matrix5(matrix):
    '''Return the canonical form of a 3x3 matrix where exactly one row and one
    column have been defined.

    >>> from math import sqrt, cos, sin
    >>> def make_euler(alpha, beta, gamma):
    ...     s1, c1 = sin(alpha), cos(alpha)
    ...     s2, c2 = sin(beta), cos(beta)
    ...     s3, c3 = sin(gamma), cos(gamma)
    ...     mat = [c2, -c3*s2, s2*s3,
    ...            c1*s2, c1*c2*c3 - s1*s3, - c3*s1 - c1*c2*s3,
    ...            s1*s2, c1*s3 + c2*c3*s1, c1*c3 - c2*s1*s3]
    ...     return mat
    >>> full_mat = make_euler(100.0, 200.0, 300.0)

    >>> some_mat = full_mat[0:4] + [None]*2 + [full_mat[6]] + [None]*2
    >>> norm_mat = normalize_matrix5(some_mat)
    >>> np.allclose(norm_mat, full_mat)
    True

    >>> some_mat = [full_mat[0]] + [None]*2 + full_mat[3:7] + [None]*2
    >>> norm_mat = normalize_matrix5(some_mat)
    >>> np.allclose(norm_mat, full_mat)
    True
    '''
    rows = matrix_rows(matrix)
    i_row, row = next((i, r) for i, r in enumerate(rows)
                      if all(x is not None for x in r))
    cols = matrix_rows(transpose(matrix))
    i_col, col = next((i, c) for i, c in enumerate(cols)
                      if all(x is not None for x in c))
    row = row[i_col:] + row[:i_col]
    col = col[i_row:] + col[:i_row]

    # row = cos(beta), -cos(gamma)sin(beta), sin(gamma)sin(beta)
    # col = cos(beta), cos(alpha)sin(beta), sin(alpha)sin(beta)
    # therefore
    sin_beta = sqrt(row[1]**2 + row[2]**2)
    cos_beta = row[0]
    if sin_beta != 0.0:
        cos_gamma = -row[1]/sin_beta
        sin_gamma = row[2]/sin_beta
        cos_alpha = col[1]/sin_beta
        sin_alpha = col[2]/sin_beta
    else:
        cos_gamma = 1.0
        sin_gamma = 0.0
        cos_alpha = 1.0
        sin_alpha = 0.0
    full = np.array([row,
                     [col[1],
                      cos_alpha*cos_beta*cos_gamma - sin_alpha*sin_gamma,
                      - cos_gamma*sin_alpha - cos_alpha*cos_beta*sin_gamma],
                     [col[2],
                      cos_alpha*sin_gamma + cos_beta*cos_gamma*sin_alpha,
                      cos_alpha*cos_gamma - cos_beta*sin_alpha*sin_gamma]])
    # reorder the rows and columns
    full = np.roll(full, shift=i_row, axis=0)
    full = np.roll(full, shift=i_col, axis=1)
    return list(full.reshape(9))


def normalize_matrix6(matrix):
    '''Return the canonical form of a 3x3 matrix where exactly two rows have
    been defined.
    '''
    matrix = matrix.copy()
    rows = matrix_rows(matrix)
    i_row = next(i for i, r in enumerate(rows) if r[0] is None)
    row_0, row_1 = rows[(i_row+1)%3], rows[(i_row+2)%3]
    row_2 = vect(row_0, row_1)
    matrix[3*i_row:3*i_row+3] = row_2
    return matrix


def transformation(trpl, surface):
    '''Apply a transformation to the given surface parameters.

    :param trpl: the transformation
    :param SurfaceMCNP surface: an MCNP surface
    '''
    if not trpl:
        return surface
    if surface.type_surface in (MS.SQ, MS.GQ):
        frame = tuple(surface.param_surface)
        params = transformation_quad(surface.compl_param, trpl)
    else:
        frame = transform_frame(surface.param_surface, trpl)
        params = list(surface.compl_param)
        if surface.type_surface in (MS.K, MS.K_X, MS.K_Y, MS.K_Z, MS.KX, MS.KY,
                                    MS.KZ):
            if len(params) == 2 or len(params) == 4:
                params.append(None)
            elif len(params) == 3 or len(params) == 5:
                params.append(params[-1])
            else:
                msg = ('Unexpected number of parameters for cone: {}'
                       .format(params))
                raise TransformationError(msg)
    return SurfaceMCNP(surface.boundary_cond, surface.type_surface, frame,
                       params, surface.idorigin)

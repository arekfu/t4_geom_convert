# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :

import numpy as np
from .TransformationError import TransformationError


def transformation_quad(params, trans):
    '''Apply the `trans` affine transformation to the quadric
    described by the `params` parameters.

    :param list(float) params: the list of 10 quadric parameters
    :param list(float) trans: the affine transformation (12 elements)
    :returns: the parameters of the transformed quadric
    :rtype: list(float)
    '''
    a_mat = np.array([[params[0], params[3] * 0.5, params[5] * 0.5, params[6] * 0.5],
                      [params[3] * 0.5, params[1], params[4] * 0.5, params[7] * 0.5],
                      [params[5] * 0.5, params[4] * 0.5,
                          params[2], params[8] * 0.5],
                      [params[6] * 0.5, params[7] * 0.5,
                          params[8] * 0.5, params[9]]
                      ])
    r_mat = np.array([[trans[3], trans[4], trans[5], 0.0],
                      [trans[6], trans[7], trans[8], 0.0],
                      [trans[9], trans[10], trans[11], 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    q_mat = np.array([[1.0, 0.0, 0.0, -trans[0]],
                      [0.0, 1.0, 0.0, -trans[1]],
                      [0.0, 0.0, 1.0, -trans[2]],
                      [0.0, 0.0, 0.0, 1.0]])
    m_mat = np.matmul(r_mat, q_mat)
    try:
        a_trans_mat = np.matmul(m_mat.T, np.matmul(a_mat, m_mat))
        params_transf = [a_trans_mat.item(0, 0),
                         a_trans_mat.item(1, 1),
                         a_trans_mat.item(2, 2),
                         a_trans_mat.item(0, 1) * 2,
                         a_trans_mat.item(1, 2) * 2,
                         a_trans_mat.item(0, 2) * 2,
                         a_trans_mat.item(0, 3) * 2,
                         a_trans_mat.item(1, 3) * 2,
                         a_trans_mat.item(2, 3) * 2,
                         a_trans_mat.item(3, 3)]
        return params_transf
    except np.linalg.LinAlgError as err:
        msg = ('Numpy error while transforming quadric {} with matrix {}: {}'
               .format(params, m_mat, err))
        raise TransformationError(msg) from None

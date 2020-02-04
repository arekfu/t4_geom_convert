# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
:file : TransformationQuad.py
'''
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
    a_mat = np.array([[params[0], params[3]*0.5, params[5]*0.5, params[6]*0.5],
                      [params[3]*0.5, params[1], params[4]*0.5, params[7]*0.5],
                      [params[5]*0.5, params[4]*0.5, params[2], params[8]*0.5],
                      [params[6]*0.5, params[7]*0.5, params[8]*0.5, params[9]]
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
                         a_trans_mat.item(0, 1)*2,
                         a_trans_mat.item(1, 2)*2,
                         a_trans_mat.item(0, 2)*2,
                         a_trans_mat.item(0, 3)*2,
                         a_trans_mat.item(1, 3)*2,
                         a_trans_mat.item(2, 3)*2,
                         a_trans_mat.item(3, 3)]
        return params_transf
    except np.linalg.LinAlgError as err:
        msg = ('Numpy error while transforming quadric {} with matrix {}: {}'
               .format(params, m_mat, err))
        raise TransformationError(msg) from None

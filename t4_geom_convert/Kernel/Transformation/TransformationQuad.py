# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019
:author: Sogeti
:data : 06 february 2019
:file : TransformationQuad.py
'''
import numpy as np

def transformationQuad(l_paramSurface, l_paramTransformation):
    l_transfParamSurface = [0,0,0,0,0,0,0,0,0,0]
    a = l_paramSurface[0]
    b = l_paramSurface[1]
    c = l_paramSurface[2]
    d = l_paramSurface[3]
    e = l_paramSurface[4]
    f = l_paramSurface[5]
    g = l_paramSurface[6]
    h = l_paramSurface[7]
    i = l_paramSurface[8]
    j = l_paramSurface[9]
    x = l_paramTransformation[0]
    y = l_paramTransformation[1]
    z = l_paramTransformation[2]
    r11 = l_paramTransformation[3]
    r12 = l_paramTransformation[4]
    r13 = l_paramTransformation[5]
    r21 = l_paramTransformation[6]
    r22 = l_paramTransformation[7]
    r23 = l_paramTransformation[8]
    r31 = l_paramTransformation[9]
    r32 = l_paramTransformation[10]
    r33 = l_paramTransformation[11]
    A = np.array([[a, d*0.5, f*0.5, g*0.5],
                    [d*0.5, b, e*0.5, h*0.5],
                    [f*0.5, e*0.5, c ,i*0.5],
                    [g*0.5, h*0.5, i*0.5, j]])
    R = np.array([[r11, r12, r13, 0],
                    [r21, r22, r23, 0],
                    [r31, r32, r33, 0],
                    [0,   0,   0,   1]])
    Q = np.array([[1, 0, 0, -x],
                    [0, 1, 0, -y],
                    [0, 0, 1, -z],
                    [0,   0,   0,   1]])
    M = np.matmul(R,Q)
    if np.linalg.det(M) != 0:
        iM = np.linalg.inv(M)
        Atransf  = np.matmul(M.T, np.matmul(A, M))
        l_transfParamSurface[0] = Atransf.item(0,0)
        l_transfParamSurface[1] = Atransf.item(1,1)
        l_transfParamSurface[2] = Atransf.item(2,2)
        l_transfParamSurface[3] = Atransf.item(0,1)*2
        l_transfParamSurface[4] = Atransf.item(1,2)*2
        l_transfParamSurface[5] = Atransf.item(0,2)*2
        l_transfParamSurface[6] = Atransf.item(0,3)*2
        l_transfParamSurface[7] = Atransf.item(1,3)*2
        l_transfParamSurface[8] = Atransf.item(2,3)*2
        l_transfParamSurface[9] = Atransf.item(3,3)
        return l_transfParamSurface
    else:
        raise ValueError('error of rotation,R%s, Q%s,  RQ %s, A %s' %(iM, A))

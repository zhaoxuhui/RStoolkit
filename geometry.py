# coding=utf-8
import numpy as np
import math


def calcR(q0, q1, q2, q3):
    m11 = 1 - 2 * q2 * q2 - 2 * q3 * q3
    m12 = 2 * q1 * q2 - 2 * q0 * q3
    m13 = 2 * q1 * q3 + 2 * q0 * q2
    m21 = 2 * q1 * q2 + 2 * q0 * q3
    m22 = 1 - 2 * q1 * q1 - 2 * q3 * q3
    m23 = 2 * q2 * q3 - 2 * q0 * q1
    m31 = 2 * q1 * q3 - 2 * q0 * q2
    m32 = 2 * q2 * q3 + 2 * 2 * q0 * q1
    m33 = 1 - 2 * q1 * q1 - 2 * q2 * q2

    R = np.zeros([3, 3], np.float)
    R[0, 0] = m11
    R[0, 1] = m12
    R[0, 2] = m13
    R[1, 0] = m21
    R[1, 1] = m22
    R[1, 2] = m23
    R[2, 0] = m31
    R[2, 1] = m32
    R[2, 2] = m33
    return R


def calcQuaternion(R):
    q0 = math.sqrt(R.trace() + 1) / 2
    q1 = (R[1, 2] - R[2, 1]) / (4 * q0)
    q2 = (R[2, 0] - R[0, 2]) / (4 * q0)
    q3 = (R[0, 1] - R[1, 0]) / (4 * q0)

    q = [q0, q1, q2, q3]
    return q
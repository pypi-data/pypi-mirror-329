from math import sin, cos
import numpy as np


def Rx(q):
    return np.array([[1,    0,          0],
                     [0,    cos(q), -sin(q)],
                     [0,    sin(q), cos(q)]])


def Ry(q):
    return np.array([[cos(q),   0,  sin(q)],
                     [0,        1,  0],
                     [-sin(q),  0,  cos(q)]])


def Rz(q):
    return np.array([[cos(q),   -sin(q),    0],
                     [sin(q),   cos(q),     0],
                     [0,        0,          1]])

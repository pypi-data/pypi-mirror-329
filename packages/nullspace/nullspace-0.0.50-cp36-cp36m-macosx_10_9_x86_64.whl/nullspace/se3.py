from sympy import sin, cos, Matrix, ZeroMatrix, BlockMatrix


def hat(r):
    return Matrix([[0, -r[2], r[1]],
                   [r[2], 0, -r[0]],
                   [-r[1], r[0], 0]])


def Ex(q):
    return Matrix([[1,  0,          0],
                   [0,  cos(q),     sin(q)],
                   [0,  -sin(q),    cos(q)]])


def Ey(q):
    return Matrix([[cos(q), 0,  -sin(q)],
                   [0,      1,  0],
                   [sin(q), 0,  cos(q)]])


def Ez(q):
    return Matrix([[cos(q),     sin(q), 0],
                   [-sin(q),    cos(q), 0],
                   [0,          0,      1]])


perfect_Ez_pi = Matrix([[-1,    0,  0],
                        [0,     -1, 0],
                        [0,     0,  1]])


def SXForm(E, r):
    return Matrix(BlockMatrix([[E, ZeroMatrix(3, 3)], [-E * hat(r), E]]))


def getE(X):
    return Matrix([[X[0, 0],    X[0, 1],    X[0, 2]],
                   [X[1, 0],    X[1, 1],    X[1, 2]],
                   [X[2, 0],    X[2, 1],    X[2, 2]]])


def getr(X):
    E = getE(X)
    leftBottomCorner = Matrix([[X[3, 0],    X[3, 1],    X[3, 2]],
                               [X[4, 0],    X[4, 1],    X[4, 2]],
                               [X[5, 0],    X[5, 1],    X[5, 2]]])
    hat = -E.T * leftBottomCorner
    return Matrix([hat[2, 1], hat[0, 2], hat[1, 0]])

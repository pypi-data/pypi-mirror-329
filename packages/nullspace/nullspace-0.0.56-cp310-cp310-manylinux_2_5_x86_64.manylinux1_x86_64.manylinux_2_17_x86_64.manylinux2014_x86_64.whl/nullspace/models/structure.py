import yaml
from sympy import eye, symbols, simplify, ZeroMatrix

from nullspace.se3 import Ex, Ey, SXForm, getr, perfect_Ez_pi


# Robot model, without link length

# q0 - q11 are all joint of legs. q0-q2 is joints of Leg0, etc.
q_sym = symbols('q0:12')
tmp1 = Ex
tmp2 = Ey


def robotBuilder(file):
    with open(file, 'r') as stream:
        try:
            out = list(yaml.safe_load(stream).values())
        except yaml.YAMLError as exc:
            print(exc)

    q_sym = symbols('q0:12')
    SX = [[SXForm(eye(3), out[0][0]),
           SXForm(eval('E' + out[0][1])(q_sym[0]), ZeroMatrix(3, 1)), SXForm(perfect_Ez_pi, out[0][2]),
           SXForm(eval('E' + out[0][3])(q_sym[1]), ZeroMatrix(3, 1)), SXForm(eye(3), out[0][4]),
           SXForm(eval('E' + out[0][5])(q_sym[2]), ZeroMatrix(3, 1)), SXForm(eye(3), out[0][6])],
          [SXForm(eye(3), out[1][0]),
           SXForm(eval('E' + out[1][1])(q_sym[3]), ZeroMatrix(3, 1)), SXForm(perfect_Ez_pi, out[1][2]),
           SXForm(eval('E' + out[1][3])(q_sym[4]), ZeroMatrix(3, 1)), SXForm(eye(3), out[1][4]),
           SXForm(eval('E' + out[1][5])(q_sym[5]), ZeroMatrix(3, 1)), SXForm(eye(3), out[1][6])],
          [SXForm(eye(3), out[2][0]),
           SXForm(eval('E' + out[2][1])(q_sym[6]), ZeroMatrix(3, 1)), SXForm(perfect_Ez_pi, out[2][2]),
           SXForm(eval('E' + out[2][3])(q_sym[7]), ZeroMatrix(3, 1)), SXForm(eye(3), out[2][4]),
           SXForm(eval('E' + out[2][5])(q_sym[8]), ZeroMatrix(3, 1)), SXForm(eye(3), out[2][6])],
          [SXForm(eye(3), out[3][0]),
           SXForm(eval('E' + out[3][1])(q_sym[9]), ZeroMatrix(3, 1)), SXForm(perfect_Ez_pi, out[3][2]),
           SXForm(eval('E' + out[3][3])(q_sym[10]), ZeroMatrix(3, 1)), SXForm(eye(3), out[3][4]),
           SXForm(eval('E' + out[3][5])(q_sym[11]), ZeroMatrix(3, 1)), SXForm(eye(3), out[3][6])]]

    ee = [[simplify(getr(SX[0][0])),
           simplify(getr(SX[0][2] * SX[0][1] * SX[0][0])),
           simplify(getr(SX[0][4] * SX[0][3] * SX[0][2] * SX[0][1] * SX[0][0])),
           simplify(getr(SX[0][6] * SX[0][5] * SX[0][4] * SX[0][3] * SX[0][2] * SX[0][1] * SX[0][0]))],
          [simplify(getr(SX[1][0])),
           simplify(getr(SX[1][2] * SX[1][1] * SX[1][0])),
           simplify(getr(SX[1][4] * SX[1][3] * SX[1][2] * SX[1][1] * SX[1][0])),
           simplify(getr(SX[1][6] * SX[1][5] * SX[1][4] * SX[1][3] * SX[1][2] * SX[1][1] * SX[1][0]))],
          [simplify(getr(SX[2][0])),
           simplify(getr(SX[2][2] * SX[2][1] * SX[2][0])),
           simplify(getr(SX[2][4] * SX[2][3] * SX[2][2] * SX[2][1] * SX[2][0])),
           simplify(getr(SX[2][6] * SX[2][5] * SX[2][4] * SX[2][3] * SX[2][2] * SX[2][1] * SX[2][0]))],
          [simplify(getr(SX[3][0])),
           simplify(getr(SX[3][2] * SX[3][1] * SX[3][0])),
           simplify(getr(SX[3][4] * SX[3][3] * SX[3][2] * SX[3][1] * SX[3][0])),
           simplify(getr(SX[3][6] * SX[3][5] * SX[3][4] * SX[3][3] * SX[3][2] * SX[3][1] * SX[3][0]))]]
    return ee

import yaml
from sympy import eye, symbols, simplify, Matrix, ZeroMatrix

from nullspace.se3 import Ex, Ey, SXForm, getr, perfect_Ez_pi


# Robot model, without link length

# q0 - q11 are all joint of legs. q0-q2 is joints of Leg0, etc.
q_sym = symbols('q0:12')

x = symbols('x0:18', real=True)
y = symbols('y0:18', real=True)
z = symbols('z0:18', real=True)

# gcLocation of 4 legs r0, r1, r2, r3
# Leg 0 structure params r6, r7, r8
# Leg 1 structure params r9, r10, r11
# Leg 2 structure params r12, r13, r14
# Leg 3 structure params r15, r16, r17
r = tuple([Matrix([x[i], y[i], z[i]]) for i in range(18)])


# XJ is the 12 joints transform in SXForm
# WARNING： Ex and Ey in XJ

XJ = [SXForm(Ex(q_sym[0]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[1]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[2]), ZeroMatrix(3, 1)),
      SXForm(Ex(q_sym[3]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[4]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[5]), ZeroMatrix(3, 1)),
      SXForm(Ex(q_sym[6]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[7]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[8]), ZeroMatrix(3, 1)),
      SXForm(Ex(q_sym[9]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[10]), ZeroMatrix(3, 1)),
      SXForm(Ey(q_sym[11]), ZeroMatrix(3, 1))]

Xtree = [None,  # 0
         None,  # 1
         None,  # 2
         None,  # 3
         None,  # 4
         None,  # 5
         SXForm(eye(3), r[6]),
         SXForm(perfect_Ez_pi, r[7]),
         SXForm(eye(3), r[8]),
         SXForm(eye(3), r[9]),
         SXForm(perfect_Ez_pi, r[10]),
         SXForm(eye(3), r[11]),
         SXForm(eye(3), r[12]),
         SXForm(perfect_Ez_pi, r[13]),
         SXForm(eye(3), r[14]),
         SXForm(eye(3), r[15]),
         SXForm(perfect_Ez_pi, r[16]),
         SXForm(eye(3), r[17])]

gcLocation = [SXForm(eye(3), r[0]),
              SXForm(eye(3), r[1]),
              SXForm(eye(3), r[2]),
              SXForm(eye(3), r[3])]


# Intermidia variable and simplify

Abad0_SX = Xtree[6]
Abad1_SX = Xtree[9]
Abad2_SX = Xtree[12]
Abad3_SX = Xtree[15]

Abad0_SX = simplify(Abad0_SX)
Abad1_SX = simplify(Abad1_SX)
Abad2_SX = simplify(Abad2_SX)
Abad3_SX = simplify(Abad3_SX)

abad0 = getr(Abad0_SX)
abad1 = getr(Abad1_SX)
abad2 = getr(Abad2_SX)
abad3 = getr(Abad3_SX)

abad0 = simplify(abad0)
abad1 = simplify(abad1)
abad2 = simplify(abad2)
abad3 = simplify(abad3)

Hip0_SX = Xtree[7] * XJ[0] * Abad0_SX
Hip1_SX = Xtree[10] * XJ[3] * Abad1_SX
Hip2_SX = Xtree[13] * XJ[6] * Abad2_SX
Hip3_SX = Xtree[16] * XJ[9] * Abad3_SX

Hip0_SX = simplify(Hip0_SX)
Hip1_SX = simplify(Hip1_SX)
Hip2_SX = simplify(Hip2_SX)
Hip3_SX = simplify(Hip3_SX)

hip0 = getr(Hip0_SX)
hip1 = getr(Hip1_SX)
hip2 = getr(Hip2_SX)
hip3 = getr(Hip3_SX)

hip0 = simplify(hip0)
hip1 = simplify(hip1)
hip2 = simplify(hip2)
hip3 = simplify(hip3)

Knee0_SX = Xtree[8] * XJ[1] * Hip0_SX
Knee1_SX = Xtree[11] * XJ[4] * Hip1_SX
Knee2_SX = Xtree[14] * XJ[7] * Hip2_SX
Knee3_SX = Xtree[17] * XJ[10] * Hip3_SX

Knee0_SX = simplify(Knee0_SX)
Knee1_SX = simplify(Knee1_SX)
Knee2_SX = simplify(Knee2_SX)
Knee3_SX = simplify(Knee3_SX)

knee0 = getr(Knee0_SX)
knee1 = getr(Knee1_SX)
knee2 = getr(Knee2_SX)
knee3 = getr(Knee3_SX)

knee0 = simplify(knee0)
knee1 = simplify(knee1)
knee2 = simplify(knee2)
knee3 = simplify(knee3)

T0 = gcLocation[0] * XJ[2] * Knee0_SX
T1 = gcLocation[1] * XJ[5] * Knee1_SX
T2 = gcLocation[2] * XJ[8] * Knee2_SX
T3 = gcLocation[3] * XJ[11] * Knee3_SX

T0 = simplify(T0)
T1 = simplify(T1)
T2 = simplify(T2)
T3 = simplify(T3)

foot0 = getr(T0)
foot1 = getr(T1)
foot2 = getr(T2)
foot3 = getr(T3)

foot0 = simplify(foot0)
foot1 = simplify(foot1)
foot2 = simplify(foot2)
foot3 = simplify(foot3)


def construct_structure(file):
    with open(file, 'r') as stream:
        try:
            out = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    links_params = {x[6]: out['abad'][0],
                    y[6]: -out['abad'][1],
                    z[6]: out['abad'][2],
                    x[7]: out['hip'][0],
                    y[7]: -out['hip'][1],
                    z[7]: out['hip'][2],
                    x[8]: out['knee'][0],
                    y[8]: out['knee'][1],
                    z[8]: out['knee'][2],
                    x[0]: 0,
                    y[0]: 0,
                    z[0]: -out['knee_link'],
                    # Leg 1
                    x[9]: out['abad'][0],
                    y[9]: out['abad'][1],
                    z[9]: out['abad'][2],
                    x[10]: out['hip'][0],
                    y[10]: out['hip'][1],
                    z[10]: out['hip'][2],
                    x[11]: out['knee'][0],
                    y[11]: out['knee'][1],
                    z[11]: out['knee'][2],
                    x[1]: 0,
                    y[1]: 0,
                    z[1]: -out['knee_link'],
                    # Leg 2
                    x[12]: -out['abad'][0],
                    y[12]: -out['abad'][1],
                    z[12]: out['abad'][2],
                    x[13]: out['hip'][0],
                    y[13]: -out['hip'][1],
                    z[13]: out['hip'][2],
                    x[14]: out['knee'][0],
                    y[14]: out['knee'][1],
                    z[14]: out['knee'][2],
                    x[2]: 0,
                    y[2]: 0,
                    z[2]: -out['knee_link'],
                    # Leg 3
                    x[15]: -out['abad'][0],
                    y[15]: out['abad'][1],
                    z[15]: out['abad'][2],
                    x[16]: out['hip'][0],
                    y[16]: out['hip'][1],
                    z[16]: out['hip'][2],
                    x[17]: out['knee'][0],
                    y[17]: out['knee'][1],
                    z[17]: out['knee'][2],
                    x[3]: 0,
                    y[3]: 0,
                    z[3]: -out['knee_link']}
    return links_params

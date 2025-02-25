from sympy import symbols, simplify
from sympy import eye, Matrix, ZeroMatrix
import yaml


from se3 import getr, SXForm, Ex, Ey, perfect_Ez_pi

q_sym = symbols('q0:12')

x0, y0, z0 = symbols('x0, y0, z0', real=True)
x1, y1, z1 = symbols('x1, y1, z1', real=True)
x2, y2, z2 = symbols('x2, y2, z2', real=True)
x3, y3, z3 = symbols('x3, y3, z3', real=True)

x6, y6, z6 = symbols('x6, y6, z6', real=True)
x7, y7, z7 = symbols('x7, y7, z7', real=True)
x8, y8, z8 = symbols('x8, y8, z8', real=True)

x9, y9, z9 = symbols('x9, y9, z9', real=True)
x10, y10, z10 = symbols('x10, y10, z10', real=True)
x11, y11, z11 = symbols('x11, y11, z11', real=True)

x12, y12, z12 = symbols('x12, y12, z12', real=True)
x13, y13, z13 = symbols('x13, y13, z13', real=True)
x14, y14, z14 = symbols('x14, y14, z14', real=True)

x15, y15, z15 = symbols('x15, y15, z15', real=True)
x16, y16, z16 = symbols('x16, y16, z16', real=True)
x17, y17, z17 = symbols('x17, y17, z17', real=True)


r0 = Matrix([x0, y0, z0])
r1 = Matrix([x1, y1, z1])
r2 = Matrix([x2, y2, z2])
r3 = Matrix([x3, y3, z3])

r6 = Matrix([x6, y6, z6])
r7 = Matrix([x7, y7, z7])
r8 = Matrix([x8, y8, z8])
r9 = Matrix([x9, y9, z9])
r10 = Matrix([x10, y10, z10])
r11 = Matrix([x11, y11, z11])
r12 = Matrix([x12, y12, z12])
r13 = Matrix([x13, y13, z13])

r14 = Matrix([x14, y14, z14])
r15 = Matrix([x15, y15, z15])
r16 = Matrix([x16, y16, z16])
r17 = Matrix([x17, y17, z17])

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
         SXForm(eye(3), r6),
         SXForm(perfect_Ez_pi, r7),
         SXForm(eye(3), r8),
         SXForm(eye(3), r9),
         SXForm(perfect_Ez_pi, r10),
         SXForm(eye(3), r11),
         SXForm(eye(3), r12),
         SXForm(perfect_Ez_pi, r13),
         SXForm(eye(3), r14),
         SXForm(eye(3), r15),
         SXForm(perfect_Ez_pi, r16),
         SXForm(eye(3), r17)]

gcLocation = [SXForm(eye(3), r0),
              SXForm(eye(3), r1),
              SXForm(eye(3), r2),
              SXForm(eye(3), r3)]

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


def links_reader(file):

    with open(file, 'r') as stream:
        try:
            out = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    links_params = {x6: out['abad_location'][0],
                    y6: -out['abad_location'][1],
                    z6: out['abad_location'][2],
                    x7: out['hip_location'][0],
                    y7: -out['hip_location'][1],
                    z7: out['hip_location'][2],
                    x8: out['knee_location'][0],
                    y8: out['knee_location'][1],
                    z8: out['knee_location'][2],
                    x0: 0,
                    y0: 0,
                    z0: -out['knee_link_length'],
                    # Leg 1
                    x9: out['abad_location'][0],
                    y9: out['abad_location'][1],
                    z9: out['abad_location'][2],
                    x10: out['hip_location'][0],
                    y10: out['hip_location'][1],
                    z10: out['hip_location'][2],
                    x11: out['knee_location'][0],
                    y11: out['knee_location'][1],
                    z11: out['knee_location'][2],
                    x1: 0,
                    y1: 0,
                    z1: -out['knee_link_length'],
                    # Leg 2
                    x12: -out['abad_location'][0],
                    y12: -out['abad_location'][1],
                    z12: out['abad_location'][2],
                    x13: out['hip_location'][0],
                    y13: -out['hip_location'][1],
                    z13: out['hip_location'][2],
                    x14: out['knee_location'][0],
                    y14: out['knee_location'][1],
                    z14: out['knee_location'][2],
                    x2: 0,
                    y2: 0,
                    z2: -out['knee_link_length'],
                    # Leg 3
                    x15: -out['abad_location'][0],
                    y15: out['abad_location'][1],
                    z15: out['abad_location'][2],
                    x16: out['hip_location'][0],
                    y16: out['hip_location'][1],
                    z16: out['hip_location'][2],
                    x17: out['knee_location'][0],
                    y17: out['knee_location'][1],
                    z17: out['knee_location'][2],
                    x3: 0,
                    y3: 0,
                    z3: -out['knee_link_length']}

    return links_params

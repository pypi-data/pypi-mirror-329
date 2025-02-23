================
Robot Descriptor
================

A quadruped

.. code:: yaml

    arm0: [
        [0.196, -0.05, 0], 'x',
        [0, -0.076, 0], 'y',
        [0, 0, -0.21], 'y',
        [0, 0, -0.19]
    ]
    arm1: [
        [0.196, 0.05, 0], 'x',
        [0, 0.076, 0], 'y',
        [0, 0, -0.21], 'y',
        [0, 0, -0.19]
    ]
    arm2: [
        [-0.196, -0.05, 0], 'x',
        [0, -0.076, 0], 'y',
        [0, 0, -0.21], 'y',
        [0, 0, -0.19]
    ]
    arm3: [
        [-0.196, 0.05, 0], 'x',
        [0,  0.076, 0], 'y',
        [0, 0, -0.21], 'y',
        [0, 0, -0.19]
    ] 


As a multi-manipulators robot, each arm in the yaml file is a manipulator.

    * The 3 dimensions list represent a link which is a Xtree
    * The string represent a joint, Xjoint, string could only be one of 'x', 'y' or 'z'.

The number of joints will be determined by how many string are there automatically. Even in quadruped
example, each line has similar format(4 links and 3 joints), it should be fine to have arbitray links
and joints. However, it has to be one link, one joint, one link...

robotBuilder take the robot each arm's linkage parameter as input and return a symbolic position with
joint variable as symbols. The return is a nested list. Each list represent one arm. And inside each list
, it is the position symbolic of each joint + ee for certain arm. For example, return[i][j] represent the symbolic position of i-th arm and j-th joint position with *q* as joint variable.

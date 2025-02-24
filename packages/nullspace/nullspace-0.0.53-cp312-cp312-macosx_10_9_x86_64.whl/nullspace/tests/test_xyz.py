import numpy as np
from nullspace.svd_wrapper import xyz


def test_xyz():
    x = np.random.random((3))
    xyz(x)

import numpy as np
import sympy as sp
from sympy import Matrix, Array

from . import rbda, se3, models

from ._version import get_versions


__version__ = get_versions()['version']
del get_versions


def ensure_positive_Z(u, vt, u_based_decision=True):
    '''
    This function is under the background of svd optimization. u or
    vt is understood as the normal vector of best fit plane of
    multi-sample points in 3d world.

    Parameters
    ----------
    u : ndarray
        u and vt are the output of 'linalg.svd' with matching inner
        dimensions so one can compute u @ vt
    vt: ndarray
        u and vt are the output of 'linalg.svd' with matching inner
        dimensions so one can compute u @ vt
    u_based_decision : bool, default=True
        If True, use the columns of u as the basis for sign flipping
        Otherwise, use the rows of v. The choice of which one is
        generally algorithm dependent.

    Returns
    -------
    u, vt : arrays with the same dimensions as the input.
    '''
    if u_based_decision:
        # sign is determined by Z location/index 2 of columns of u
        sign = np.sign(u[-1][2])
    else:
        # sign is determined by Z location/index 2 of rows of vt
        sign = np.sign(vt[-1, :][2])

    # Convert u to positive if it's negative, stay positive if not
    u[:, -1] *= sign
    # Make sure u and vt sign change together so that matrix multiplication
    # result won't change.
    vt[-1, :] *= sign
    return u, vt


def svd_without_sign_ambiguity(a):
    '''
    SVD with ensure deterministic.

    The raw svd function of numpy only ensure the multiplication result of
    column of u and matching row of vt is deterministic. If there is a matrix
    a in shape (M, N), both pair of (u[:, k], vt[k, :]) and pair of (-u[:,k],
    -vt[k, :]) are possible returned pair, where k = range(K), K = min(M, N).
    The sign ambiguity could exist for a pair of column u and matching a row
    of vt.
    The sign of each columns of u and each rows of vt are determined by a
    measure of left singular vector(u) with X and a measure of right singular
    vector(vt) with X. If they disagree with each other, the one with bigger
    abs value will be choose as determining factor, hence need to be always
    positive, and the other one will be flipped coorespondingly.
    This function implicitly use 'full_matrices=False'

    Parameters
    ----------
    a : (M, N) array
        A numpy 2D matrix, which should be legal for SVD. The legal check is
        handled by 'numpy.linalg.svd' inside function.

    Returns
    -------
    u : (M, K) array
        Left singular vectors. K = min(M, N)
    s: (, K) array
        Vector with the singular values.
    vt: (K, N) array
        Right singular vectors.

    References
    ----------
    .. [1] Bro, R., Acar, E., & Kolda, T. G. (2008). Resolving
           the sign ambiguity in the singular value decomposition
           Journal of Chemometrics: A Journal of the Chemometrics
           Society, 22(2), 135-140.
    .. [2] https://prod-ng.sandia.gov/techlib-noauth/access-control.cqi/2007/076422.pdf
    '''
    # svd dimensions:
    # u, s, vt = np.linalg.svd(X, full_matrices=False)
    # a = u @ diag(s) @ vt
    # (M, N) = (M, K) @ (K, K) @ (K, N)

    u, s, vt = np.linalg.svd(a, full_matrices=False)

    M = u.shape[0]
    N = vt.shape[1]
    K = s.shape[0]

    assert u.shape == (M, K)
    assert vt.shape == (K, N)
    assert a.shape == (M, N)

    sign_dict = {'left': np.zeros(K),
                 'right': np.zeros(K)}

    for k in range(K):
        mask = np.ones(K).astype(bool)
        mask[k] = False
        # (M, N) = (M, N) (M, K-1) @ (K-1, K-1) @ (K-1, N)
        Y = a - (u[:, mask] @ np.diag(s[mask]) @ vt[mask, :])
        for j in range(N):
            d = np.dot(u[:, k], Y[:, j])
            sign_dict['left'][k] += np.sum(np.sign(d) * d**2)
        for i in range(M) :
            d = np.dot(vt[k, :], Y[i, :])
            sign_dict['right'][k] += np.sum(np.sign(d) * d**2)

    for k in range(K):
        sign = 1.0
        if sign_dict['left'][k] < 0 and sign_dict['right'][k] < 0:
            sign = -1.0
        elif sign_dict['left'][k] * sign_dict['right'][k] < 0:
            if abs(sign_dict['left'][k]) < abs(sign_dict['right'][k]):
                # Use sign of right as determining flip sign.
                sign = np.sign(sign_dict['right'][k])
            else:
                sign = np.sign(sign_dict['left'][k])
        # multiplied by sign of itself will always change it to positive
        u[:, k] = u[:, k] * sign
        # alwars flip together.
        vt[k, :] = vt[k, :] * sign
    return u, s, vt


def svd_regulated(a):
    '''
    Wrapper function takes care of the replacement of standard svd
    to achieve goals below.
    1. sign of deterministic of svd
    2. In 3D world, the optimized normal vector achieved by svd is
    roughly aligned with Z-ish axis.

    The first goal is much more important in autodiff_svd. The second
    make sure normal vector only change in positive Z semi-space in
    3d. This make sure normal vector won't jog. This function implicityly
    return with 'full_matrices=False'
    '''
    u, s, vt = svd_without_sign_ambiguity(a)
    if a.shape[0] < a.shape[1]:  # bus
        u, vt = ensure_positive_Z(u, vt)
    else:  # rocket
        u, vt = ensure_positive_Z(u, vt, u_based_decision=False)
    return u, s, vt


def autodiff_svd(A, q_star, *, symbolic=False):
    '''
    Automatic Differentiating of svd.

    It takes matrix A, return differentiation of U, S and V with respect to
    specific q value q_star. U, S and VT(V.T) are result of standard SVD.
    This method is implemented in reverse mode in terms of auto diff conventions
    which is more effeciency since all free variables q take advantages of same
    intermedia svd result, U_star, S_star and V_star. It returns ecomonic result
    which means 'full_matrices=False' in corresponding 'numpy.linalg.svd'

    Parameters
    ----------
    A : (m, n) Matrix
        A sympy symbolic 2D Matrix, which should be legal for SVD later.
    q_star : dict
        A dict from sympy symbolic variable to value.
    symbolic : bool, optional
        Control return type. Return numerical result, numpy.ndarray, if true
        (default), otherwise return symbolic result, sympy.Array.

    Returns
    -------
    du : (Q, M, K) array
        Partial derivatives/gradient of U with respect to each variables in q star.
        Each variable matches a (M, K) matrix. Q is number of variables. Return
        sympy.Array if symbolic=True.
    ds : (0, K, K) array
        Partial derivatives/gradient of S with respect to each variables in q star,
        Each variable matches a (M, K) matrix. K = min(M, N). (..., K, K) is a strict
        diagonal matrix which is quaranteed by Hadamard operation. check examples
        for details. Return 'sympy.Array' if symbolic=True.
    dv : (Q, N, K) array
        Partial derivatives/gradient of V(NOT VT) with respect to each variables in
        q_star. Each variable matches a (N, K) matrix. Return 'sympy.Array' if
        symbolic=True

    See Also
    --------
    numpy.linalg.svd : Similar function in numpy.
    sympy.Array : 3D tensor in sympy.
    sympy.Matrix.jacobian : jacobian calculation in sympy.

    References
    ----------
    .. [1] James Townsend. Differentiating the Singular Value Decomposition.
    .. [2] Mike Giles. An extended collection of matrix derivative results
       for forward and reverse mode algorithmic differentiation.

    Examples
    --------
    >>> from sympy import sin, cos, symbols, Matrix
    >>> q0, q1 = symbols ("q0, q1")
    ... q star = (q0: 1, q1: 2}
    ... A = Matrix([[2*q0,          1,    q0**3 + 2*q1, sin(q0) + q1],
                   [q0**2 - q1**2,  2*q1, 2*q0 + q1**3, cos(q0) + q1],
                   [q0**2 + q1**2,  2,    3,            sin(q0) + cos(q1)]])
    >>> du, ds, dv = autodiff svd(A, q_star)
    >>> du.shape
    (2, 3, 3)
    >>> ds.shape
    (2, 3, 3)
    >>>dv.shape
    (2, 4, 3)
    >>> du_sym, ds_sym, dv_sym = autodiff_svd(A, q_star, symbolic=True)
    '''
    M, N = A.shape
    K = min(M, N)
    Q = len(q_star)
    # For a specific q0 and q1, get U_star, S_star and V_star_T.
    A_star = np.array(A.subs(q_star), dtype=float)
    U_star, S_star_1d, V_star_T = svd_regulated(A_star)  # U star (m, k), S star 1d (k, 1),
    U_star = U_star[:, :K]  # Use economic U (m, k)
    V_star_T = V_star_T[:K, :]  # Use economic VT (k, n)
    S_star = np.diag(S_star_1d)  # Construct S (k, k)
    S_star_inv = np.diag(np.reciprocal(S_star_1d))
    Ik = sp.eye(K)
    U_star_T = U_star.T
    V_star = V_star_T.T

    # F
    F_star = Matrix([[0 if i == j else 1 / (S_star_1d[j]**2 - S_star_1d[i]**2)
                    for j in range(K)]
                    for i in range(K)])

    # dA
    # Reshape A to 1d vector for convenience of jacobian calculation, will reshape back to 2
    A_element_wise = A.reshape(M * N, 1)

    q_var = Matrix(list(q_star.keys()))  # (g 0, q 1, qi. .., q Q-1]
    dA_element_wise = A_element_wise.jacobian(q_var)  # in shape (m*n, Q)
    # Reserve list of dA, d5, du and dv for each q variables. E.X. dA lsti] is dA with resp
    dA_lst = [None] * Q
    ds_lst = [None] * Q
    du_lst = [None] * Q
    dv_lst = [None] * Q

    Im = sp.eye(M)
    In = sp.eye(N)
    for i in range(Q):
        # Get matrix dA of eq(6) wrt qi, each element in dA lst is dA wrt qi. dA wrt gi is
        dA_lst[i] = dA_element_wise.T[i, :].reshape(M, N)
        # Use @ instead of * force all binary operation between np.array(s) and sp.Matrix(s)
        du_lst[i] = U_star @ F_star.multiply_elementwise(U_star_T @ dA_lst[i] @ V_star @ S_star
                                                         + S_star @ V_star_T @ dA_lst[i].T @ U_star) \
            + (Im - U_star @ U_star_T) @ dA_lst[i] @ V_star @ S_star_inv
        ds_lst[i] = Ik.multiply_elementwise(U_star_T @ dA_lst[i] @ V_star)
        dv_lst[i] = V_star @ F_star.multiply_elementwise(S_star @ U_star_T @ dA_lst[i] @ V_star
                                                         + V_star_T @ dA_lst[i].T @ U_star @ S_star) \
            + (In - V_star @ V_star_T) @ dA_lst[i].T @ U_star @ S_star_inv
    # Build a 3D tensor for all q variables
    du_tensor = Array([e.tolist() for e in du_lst])  # (Q, M, K)
    ds_tensor = Array([e.tolist() for e in ds_lst])  # (Q, K, K)
    dv_tensor = Array([e.tolist() for e in dv_lst])  # (Q, N, K)

    if symbolic:
        return du_tensor, ds_tensor, dv_tensor
    else:
        return (np.array(du_tensor.subs(q_star), dtype=float),
                np.array(ds_tensor.subs(q_star), dtype=float),
                np.array(dv_tensor.subs(q_star), dtype=float))

import numpy as np
import matplotlib.pyplot as plt


# Lagrange interpolant
def lagrange_basis(x, xk, n, k):
    Lnk = np.array([(x - xk[j]) / (xk[k] - xk[j]) for j in range(n + 1) if j != k]).prod(axis=0)
    return Lnk

def p(x, xk, n):
    pn = np.array([f(xk[k]) * lagrange_basis(x, xk, n, k) for k in range(n + 1)]).sum(axis=0)
    return pn


def get_cheby_nodes(x, n):
    a = x[0]
    b = x[-1]
    xk = np.array([np.cos((2 * k - 1) / (2 * n) * np.pi) for k in np.arange(1, n+1)])
    xk = 0.5 * ((b - a) * xk + a + b)
    return xk


def second_bary_with_cheby(x, f, n):
    xk = get_cheby_nodes(x, n + 1)
    
    if type(f).__name__ == 'function':
        f = f(xk)
    
    numer_mat = []
    denom_mat = []
    for k in range(n + 1):
        const = 0.5 if (k == 0) or (k == n) else 1.
        numer_mat.append(const * ((-1)**k * f[k]) / (x - xk[k]))
        denom_mat.append(const * (-1)**k / (x - xk[k]))
    
    numer = np.array(numer_mat).sum(axis=0)
    denom = np.array(denom_mat).sum(axis=0)
    return numer / denom
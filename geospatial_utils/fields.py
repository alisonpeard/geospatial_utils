"""https://pieterjanrobbe.github.io/GaussianRandomFields.jl/dev/tutorial/"""

import numpy as np
from numbers import Number
from itertools import product
from scipy.spatial import distance_matrix
from scipy.special import gamma, kv


def cosine_cov(dx, l=1):
    return np.cos(2 * np.pi * dx / l)


def exp1d_cov(dx, l=0.1, σ=1):
    return σ * np.exp( -dx / l)


def matern_cov(dx, l=1, nu=.5, eps=1e-5):
    x = np.sqrt(2 * nu) * dx / l
    C = (1 / (gamma(nu) * 2**(nu-1))) * (x**nu) * kv(nu, x + eps)
    return C


def gaussian_random_field(nx, ny, l=10, mean=0, var=1, cov=cosine_cov, **kwargs):
    """Sample a basic Gaussian random field using cosine covariance."""
    n = nx * ny
    if isinstance(mean, Number):
        mean = mean * np.ones(n)
    coords = np.array(list(product(range(ny), range(nx))))
    dmat = distance_matrix(coords, coords)
    cmat = cov(dmat, l=l, **kwargs)
    grf = np.random.multivariate_normal(mean, var * cmat)
    return grf.reshape([ny, nx])
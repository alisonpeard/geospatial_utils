"""https://pieterjanrobbe.github.io/GaussianRandomFields.jl/dev/tutorial/"""

import numpy as np
from numbers import Number
from itertools import product
from scipy.spatial import distance_matrix
from scipy.fft import idctn
# from scipy.special import gamma, kv


def cosine_cov(dx, l=1):
    return np.cos(2 * np.pi * dx / l)


def exp1d_cov(dx, l=0.1, σ=1):
    return σ * np.exp( -dx / l)


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


def matern_grf(n, tau, alpha):
    """Return a sample of a Gaussian random field on [0,1]^2.
    
    with:
    mean 0
    covariance operator C = (-Delta + tau^2)^(-alpha)
    where Delta is the Laplacian with zero Neumann boundary conditions.
    
    adapted from: https://github.com/neuraloperator/neuraloperator/blob/master/data_generation/darcy/GRF.m
    """
    xi = np.random.normal(0, 1, (n, n))
    K1, K2 = np.meshgrid(range(n), range(n))
    coef = tau**(alpha-1) * (np.pi**2 * (K1**2 + K2**2) + tau**2)**(-alpha/2)
    L = n * coef * xi
    L[0, 0] = 0
    U = idctn(L, norm='ortho')
    return U
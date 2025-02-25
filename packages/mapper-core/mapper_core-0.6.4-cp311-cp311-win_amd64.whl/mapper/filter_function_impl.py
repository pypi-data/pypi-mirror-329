# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

from typing import Callable

import numpy as np
from numba import float32, int32, jit


def get_lp_eccentricity_fn(
    metric: Callable[[np.ndarray, np.ndarray], np.float32], p: float = 1.0
):
    """Get a function that computes l^p eccentricity wrt a given metric.

    The returned function is compiled with numba, and expects a C-contiguous 2d
    float32 array whose rows are datapoints.

    The metric argument should be a numba-compiled function that takes two
    contiguous 1d arrays and computes the distance between them.
    """
    # TODO: parallelize
    if p < np.inf:

        @jit(float32[::1](float32[:, ::1]), nopython=True)
        def lp_eccentricity(X: np.ndarray):
            N = X.shape[0]
            ecc = np.zeros(N, dtype=np.float32)
            for i in range(N):
                e = 0.0
                for j in range(N):
                    e += metric(X[i, :], X[j, :]) ** p
                ecc[i] = e ** (1 / p)
            return ecc

        return lp_eccentricity
    else:

        @jit(float32[::1](float32[:, ::1]), nopython=True)
        def linf_eccentricity(X: np.ndarray):
            N = X.shape[0]
            ecc = np.zeros(N, dtype=np.float32)
            for i in range(N):
                e = 0.0
                for j in range(N):
                    next_e = metric(X[i, :], X[j, :])
                    if next_e > e:
                        e = next_e
                ecc[i] = e
            return ecc

        return linf_eccentricity


def get_gaussian_density_fn(metric: Callable[[np.ndarray, np.ndarray], np.float32]):
    """Get a function that computes Gaussian density wrt a given metric.

    The returned function is compiled with numba, and expects a C-contiguous 2d
    float32 array whose rows are datapoints.

    The metric argument should be a numba-compiled function that takes two
    contiguous 1d arrays and computes the distance between them.
    """

    # TODO: parallelize
    @jit(float32[::1](float32[:, ::1]), nopython=True)
    def gaussian_density(X: np.ndarray):
        N = X.shape[0]
        mean = 0.0
        for i in range(N):
            for j in range(i):
                mean += metric(X[i, :], X[j, :])
        mean *= 2 / (N * (N - 1))

        density = np.zeros(N, dtype=np.float32)
        if mean < 1e-6:
            return density
        for i in range(N):
            for j in range(i):
                dij = metric(X[i, :], X[j, :])
                wij = np.exp(-(dij**2) / mean**2)
                density[i] += wij
                density[j] += wij

        return density

    return gaussian_density


@jit(float32[::1](int32[:, ::1], float32[:, ::1]), nopython=True)
def gaussian_nbrs_density(
    neighbors: np.ndarray,
    distances: np.ndarray,
):
    """Compute an estimate of the Gaussian density of a dataset from an nn-graph.

    Uses only the nearest neighbors given in the graph to approximate the
    density at each point. These are the largest terms in the sum, so should be
    a reasonable approximation.
    """

    N, K = neighbors.shape

    mean = 0.0
    for i in range(N):
        for jdx in range(K):
            dij = distances[i, jdx]
            mean += dij
    mean /= N * K

    density = np.zeros(N, dtype=np.float32)
    for i in range(N):
        for jdx in range(K):
            dij = distances[i, jdx]
            density[i] += np.exp(-(dij**2) / mean**2)

    return density

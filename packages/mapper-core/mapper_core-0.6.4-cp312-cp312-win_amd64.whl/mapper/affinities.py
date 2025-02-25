# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++
"""Functions for computing edge weights from (normalized) distances."""


from typing import Callable, Dict

import cython
import numpy as np
from cython.cimports.libc.math import e, exp, log, sqrt


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.exceptval(check=False)
def distances_to_affinities_slpi(distances: cython.float[::1]) -> np.ndarray:
    """SLPI stands for Sqrt(log()) Plus Inverse. See `src/xshop/graph/NbrsGraph.java`"""
    affinities: cython.float[::1] = np.empty_like(distances, dtype=np.float32)
    min_distance = 1e-4
    max_affinity = sqrt(-log(min_distance))
    # bounds: i < len(distances) = len(affinities)
    for i in range(len(distances)):
        if distances[i] < min_distance:
            affinities[i] = max_affinity
        elif distances[i] <= 1 / e:
            affinities[i] = sqrt(-log(distances[i]))
        else:
            affinities[i] = 1 / (distances[i] * e)
    return np.asarray(affinities)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.exceptval(check=False)
def distances_to_affinities_expinv(distances: cython.float[::1]) -> np.ndarray:
    """Exponential function for weights down to 0.01, with 1/x decay after that."""
    affinities = np.empty_like(distances)
    affinities_view: cython.float[::1] = affinities
    i: cython.Py_ssize_t
    N: cython.Py_ssize_t = len(distances)
    # bounds: i < len(distances) = len(affinities)
    for i in range(N):
        if distances[i] <= log(100):
            affinities_view[i] = exp(-distances[i])
        else:
            affinities_view[i] = (log(100) / 100) / distances[i]
    return affinities


def distances_to_affinities_exponential(distances: np.ndarray) -> np.ndarray:
    affinities = np.exp(-(distances))
    return affinities


def distances_to_affinities_gaussian(distances: np.ndarray) -> np.ndarray:
    affinities = np.exp(-(distances**2))
    return affinities


affinity_functions: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
    "slpi": distances_to_affinities_slpi,
    "exponential": distances_to_affinities_exponential,
    "expinv": distances_to_affinities_expinv,
    "gaussian": distances_to_affinities_gaussian,
}

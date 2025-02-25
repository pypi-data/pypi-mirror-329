# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++
"""Various classes producing filter functions."""

from abc import abstractmethod
from typing import Callable, Literal, Optional, Union

import numpy as np

from mapper.distances import _get_metric_fn
from mapper.filter_function_impl import (
    gaussian_nbrs_density,
    get_gaussian_density_fn,
    get_lp_eccentricity_fn,
)
from mapper.matrix import MapperMatrix
from mapper.neighborgraph import KNNGraph


class FilterFunction:
    """Represents the data source and params for a Filter object.

    Abstract, with various concrete child classes with different ways of
    producing filter function values.
    """

    def __init__(
        self,
        source_matrix: MapperMatrix,
    ):
        """Params:
        source_matrix: a MapperMatrix object representing the source data from
        which this was derived.
        """
        if isinstance(source_matrix, np.ndarray):
            source_matrix = MapperMatrix(source_matrix)
        self.source_matrix = source_matrix

    @property
    @abstractmethod
    def f_vals(self) -> np.ndarray:
        """Return the f_vals. Select the col/row from source_data if necessary, or
        compute."""

    def __len__(self) -> int:
        """Allows len(filter_source); returns len(f_vals) or 0 if None."""
        return len(self.f_vals)


# pylint: disable=invalid-name
def FilterSource(
    source_matrix: Union[MapperMatrix, np.ndarray],
    method: Literal[
        "eccentricity",
        "density",
        "nbrs_density",
        "raw_vals",
    ] = "raw_vals",
    ecc_p=None,
    f_vals: Optional[np.ndarray] = None,
    metric: Optional[Union[str, Callable]] = None,
    nbr_graph: Optional[KNNGraph] = None,
) -> FilterFunction:
    """Construct an appropriate FilterFunction object given the parameters.

    This is a compatibility shim, and should not be used in new code.

    Params:
    source_matrix: a MapperMatrix object representing the source data from
    which this was derived.

    method: string literal indicating the filter function method/type.

    ecc_p: float indicating the value p used in l^p eccentricity computation

    f_vals: np.ndarray of float32s of filter function values at each point.

    metric: string or numba-compiled function representing the metric to be
    used in computing f_vals.

    nbr_graph: NeighborGraph if needed for density f computation.
    """

    if isinstance(source_matrix, np.ndarray):
        source_matrix = MapperMatrix(source_matrix)
    if method not in [
        "eccentricity",
        "density",
        "nbrs_density",
        "raw_vals",
    ]:
        raise ValueError(f"Unknown FilterSource method {method}.")

    if method == "density":
        if metric is None:
            raise ValueError("Must specify a metric for method=density.")
        else:
            return DensityFunction(source_matrix, metric, nbr_graph)
    if method == "eccentricity":
        if metric is None or ecc_p is None:
            raise ValueError("Must specify metric and ecc_p for method=eccentricity.")
        else:
            return EccentricityFunction(source_matrix, ecc_p, metric)
    if method == "nbrs_density":
        if nbr_graph is None:
            raise ValueError("Must specify a nbr_graph for method=nbrs_density.")
        return DensityFunction(source_matrix, "euclidean", nbr_graph)
    if method == "raw_vals":
        if f_vals is None:
            raise ValueError("Must provide f_vals for method=raw_vals.")
        return RawFunction(source_matrix, f_vals)


class EccentricityFunction(FilterFunction):
    """The l^p eccentricity of each point in a dataset with respect to a given
    metric.
    """

    def __init__(
        self,
        source_matrix: MapperMatrix,
        p: Union[float, int],
        metric: Union[str, Callable],
    ):
        super().__init__(source_matrix)
        self.p = float(p)
        if self.p < 1:
            raise ValueError(f"p (={p}) must be >= 1")
        if np.isnan(self.p):
            raise ValueError("p may not be nan")
        self.metric = _get_metric_fn(metric)
        self._f_vals: Optional[np.ndarray] = None

    def _compute_eccentricity(self) -> np.ndarray:
        self.ecc_fn = get_lp_eccentricity_fn(self.metric, self.p)
        return self.ecc_fn(self.source_matrix.X)

    @property
    def f_vals(self) -> np.ndarray:
        if self._f_vals is None:
            self._f_vals = self._compute_eccentricity()
        return self._f_vals

    def __repr__(self) -> str:
        return (
            f"EccentricityFunction(source_data={self.source_matrix}, "
            f"p={self.p}, metric={self.metric})"
        )


class DensityFunction(FilterFunction):
    """A local estimate of the density at each point in a dataset using a
    Gaussian kernel.
    """

    def __init__(
        self,
        source_matrix: MapperMatrix,
        metric: Union[str, Callable],
        nbrs_graph: Optional[KNNGraph] = None,
    ):
        super().__init__(source_matrix)
        self.metric = _get_metric_fn(metric)
        self.nbrs_graph = nbrs_graph
        self._f_vals: Optional[np.ndarray] = None

    def _compute_density(self) -> np.ndarray:
        if self.nbrs_graph is not None:
            # pylint: disable=protected-access
            return gaussian_nbrs_density(
                self.nbrs_graph._neighbors,
                self.nbrs_graph._distances,
            )
        else:
            self.density_fn = get_gaussian_density_fn(self.metric)
            return self.density_fn(self.source_matrix.X)

    @property
    def f_vals(self) -> np.ndarray:
        if self._f_vals is None:
            self._f_vals = self._compute_density()
        return self._f_vals

    def __repr__(self) -> str:
        return (
            f"DensityFunction(source_data={self.source_matrix}, "
            f"metric={self.metric}, use_nbrs={self.nbrs_graph is not None})"
        )


class RawFunction(FilterFunction):
    """An arbitrary user-provided function on a dataset."""

    def __init__(self, source_matrix: MapperMatrix, f_vals: np.ndarray):
        super().__init__(source_matrix)
        self._check_f_vals(f_vals)
        self._f_vals = np.ascontiguousarray(f_vals, dtype=np.float32)

    def _check_f_vals(self, f_vals: np.ndarray):
        """Sanity check for an array of f_vals."""
        # Enforce sane initializations
        if f_vals.ndim != 1:
            raise ValueError("f_vals must be a 1-dimensional array")
        if np.any(np.isnan(f_vals)):
            raise ValueError("Filter function values may not be NaN.")
        if np.any(np.isinf(f_vals)):
            raise ValueError("Filter functions may not have infinite values.")
        if len(f_vals) != self.source_matrix.shape[0]:
            raise ValueError(
                f"len(f_vals)={len(f_vals)} doesn't match source_data "
                f"N={self.source_matrix.shape[0]}."
            )

    @property
    def f_vals(self) -> np.ndarray:
        return self._f_vals

    def __repr__(self) -> str:
        return f"RawFunction(source_data={self.source_matrix}, len={len(self)})"

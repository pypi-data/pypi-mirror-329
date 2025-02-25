# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++
"""Partition nodes according to one or more filter functions."""

import math
from abc import abstractmethod
from typing import Literal, Optional, Union

import cython
import numpy as np
from cython.cimports.libc.stdint import int32_t

from mapper.filter_function import FilterFunction
from mapper.matrix import MapperMatrix
from mapper.neighborgraph import (
    FunctionValuePruningPredicate,
    GraphPruningPredicate,
    LocalFunctionValuePruningPredicate,
    PercentOverlapPruningPredicate,
    TrivialPruningPredicate,
)


class DataPartition:
    """Abstract class representing a way of splitting a NeighborGraph into bins.
    This may or may not be based on a FilterFunction.
    """

    n_bins: int

    @property
    @abstractmethod
    def domain_partition(self) -> np.ndarray:
        """An array of length len(self.filter_source) with entries in range(0,
        self.n_bins) indicating which bin each data point falls in.
        """

    @property
    @abstractmethod
    def pruning_predicate(self) -> GraphPruningPredicate:
        """A GraphPruningPredicate instance that provides a method to mask off
        undesired edges of a CSRNeighborGraph."""


# A filter function on a dataset X with N points is just a length-N float array.
# (the f_vals property of a FilterFunction) We need to partition the range of
# such a function, with a few options: One ("rng") is to partition the range
# into T equal-length subintervals.  The other ("uni") is to partition the range
# into T subintervals so that each contains an equal number of unique function
# values.

# The partition of the filter range is represented by a float array B of length
# T+1 containing the boundary points for each interval in the partition.  To be
# more precise, the ith partition interval is the half-open interval
# [B[i], B[i+1]). This means that the last entry of B needs to be slightly
# greater than the maximum value of f, accomplished here with np.nextafter().

# We need to pull this partition back to X, by finding the index of the
# subinterval that contains each point.

# We need to remember these indices and possibly the filter function
# quantiles in order to do pruning later.


class Filter(DataPartition):
    """A standard filter, partitioning the dataset based on the values of a 1-d
    FilterFunction.

    When created, stores the FilterFunction and configuration parameters, but
    does not compute the domain partition in case the FilterFunction is
    expensive to compute.  This object is meant to be immutable and
    reconstructed when a new Filter is necessary.
    """

    def __init__(
        self,
        filter_source: FilterFunction,
        n_bins: int,
        bin_method: Literal["rng", "uni"] = "rng",
        pruning_method: Literal["bin", "pct", "frac"] = "bin",
        pruning_threshold: Union[int, float] = 1,
        name: Optional[str] = None,
    ):
        """Params:

        filter_source: FilterSource object referencing the source MapperMatrix
        and a filter method, column index if relevant, and function vals for each
        point.

        n_bins: the number of sets into which to partition the range of the
        filter function.

        bin_method: how to divide the range into bins. If "rng", the range
        of the filter function will be divided into n_bins intervals of
        equal length. If "uni", the range will be divided into n_bins
        intervals containing an equal number of unique filter values (except
        the uppermost bin, which may have a smaller number).

        pruning_method: a strategy for pruning edges of the neighborhood graph
        based on the filter values. If "bin", edges that go between filter bins
        separated by some threshold value will be removed. If "pct", edges that
        go between nodes with filter values that belong to percentiles of the
        filter function separated by some threshold will be removed. If "frac",
        will only preserve edges that go between data points within a certain
        distance of the boundary between adjacent bins.

        pruning_threshold: the threshold for pruning edges according to
        pruning_method. This should be an integer if "bin", representing the
        maximum difference in bin level, and a float between 0 and 1 if
        "pct", representing the maximum difference in filter function
        quantiles.

        name: an optional name for the filter, used when displaying a
        representation of the filter.
        """

        if len(filter_source) < 1:
            raise ValueError("Expected FilterFunction of length > 0")
        self.filter_source = filter_source
        self.N = len(self.filter_source)

        if n_bins < 1:
            raise ValueError("Expected one or more partition bins.")
        self.n_bins = n_bins

        if bin_method not in ["rng", "uni"]:
            raise ValueError("bin_method must be one of 'rng' or 'uni'")
        self.method = bin_method

        if pruning_method not in ["bin", "pct", "frac"]:
            raise ValueError("pruning_method must be one of 'bin', 'pct', or 'frac'")
        self.pruning_method = pruning_method

        if pruning_threshold < 0:
            raise ValueError("pruning_threshold must be nonnegative")
        self.pruning_threshold = pruning_threshold

        self.name = name if name else "filter"

        # TODO: use more descriptive names for these methods?

        self._range_partition: Optional[np.ndarray] = None
        self._domain_partition: Optional[np.ndarray] = None
        self._prune_vals: Optional[np.ndarray] = None
        self._pruning_predicate: Optional[GraphPruningPredicate] = None

    @property
    def f(self) -> np.ndarray:
        return self.filter_source.f_vals

    @property
    def range_partition(self) -> np.ndarray:
        if self._range_partition is None:
            if self.method == "rng":
                self._range_partition = partition_filter_range_rng(self.f, self.n_bins)
            else:
                self._range_partition = partition_filter_range_uni(self.f, self.n_bins)
        return self._range_partition

    @property
    def domain_partition(self) -> np.ndarray:
        if self._domain_partition is None:
            self._domain_partition = partition_filter_domain(
                self.filter_source.f_vals, self.range_partition
            )
        return self._domain_partition

    @property
    def prune_vals(self) -> np.ndarray:
        if self._prune_vals is None:
            if self.pruning_method == "bin":
                self._prune_vals = self.domain_partition
            elif self.pruning_method == "pct":
                self._prune_vals = get_filter_quantiles(self.f)
            else:
                raise ValueError("prune_vals not valid when pruning_method='frac'")
        return self._prune_vals

    @property
    def pruning_predicate(self):
        if self._pruning_predicate is None:
            if self.pruning_method == "frac":
                self._pruning_predicate = PercentOverlapPruningPredicate(
                    self.f,
                    self._range_partition,
                    self._domain_partition,
                    self.pruning_threshold,
                )
            else:
                prune_vals = self.prune_vals
                pruning_threshold = self.pruning_threshold
                self._pruning_predicate = FunctionValuePruningPredicate(
                    prune_vals, pruning_threshold
                )

        return self._pruning_predicate

    @property
    def parent_dataset(self) -> MapperMatrix:
        """Return the parent dataset for this Filter."""
        return self.filter_source.source_matrix

    def __repr__(self):
        return "\n".join(
            [
                f"[filter {self.name}: bins={self.n_bins}, method={self.method}, "
                f"pruning={self.pruning_method}, gain={self.pruning_threshold}]",
                f"{self.filter_source}",
            ]
        )


class TrivialFilter(DataPartition):
    """A trivial filter with one bin and no edge pruning."""

    def __init__(self, source_matrix: MapperMatrix):
        self.source_matrix = source_matrix
        self.n_bins = 1

        self._domain_partition: Optional[np.ndarray] = None
        self._pruning_predicate = TrivialPruningPredicate()

    @property
    def domain_partition(self) -> np.ndarray:
        if self._domain_partition is None:
            self._domain_partition = np.zeros(
                self.source_matrix.shape[0], dtype=np.int32
            )
        return self._domain_partition

    @property
    def pruning_predicate(self) -> GraphPruningPredicate:
        return self._pruning_predicate


class LocalFilter(Filter):
    """A data partition based on a FilterFunction that is only applied to a
    subset of data points.

    The domain argument is an array of indices into the underlying
    FilterFunction, which means it should not consist of row/column ids from the
    original Dataset, but from the MapperMatrix.

    Divides the domain into n_bins sets when constructing bins, ignoring all
    other data points. This makes it different from restricting the partition
    created by a Filter to a subset of points.
    """

    def __init__(
        self,
        filter_source: FilterFunction,
        domain: np.ndarray,
        n_bins: int,
        bin_method: Literal["rng", "uni"] = "rng",
        pruning_method: Literal["bin", "pct"] = "bin",
        pruning_threshold: Union[int, float] = 1,
        name: Optional[str] = None,
    ):
        super().__init__(
            filter_source, n_bins, bin_method, pruning_method, pruning_threshold, name
        )

        if np.max(domain) > len(filter_source) - 1:
            raise ValueError("domain contains points not in the filter source domain")
        self.domain = domain

    @property
    def range_partition(self) -> np.ndarray:
        if self._range_partition is None:
            if self.method == "rng":
                self._range_partition = partition_filter_range_rng(
                    self.filter_source.f_vals[self.domain], self.n_bins
                )
            else:
                self._range_partition = partition_filter_range_uni(
                    self.filter_source.f_vals[self.domain], self.n_bins
                )
        return self._range_partition

    @property
    def domain_partition(self) -> np.ndarray:
        if self._domain_partition is None:
            restricted_domain_partition = partition_filter_domain(
                self.filter_source.f_vals[self.domain], self.range_partition
            )
            domain_partition = np.full_like(
                self.filter_source.f_vals,
                restricted_domain_partition.max() + 1,
                dtype=np.int32,
            )
            domain_partition[self.domain] = restricted_domain_partition
            self._domain_partition = domain_partition
        return self._domain_partition

    @property
    def prune_vals(self) -> np.ndarray:
        if self._prune_vals is None:
            if self.pruning_method == "bin":
                self._prune_vals = self.domain_partition
            else:  # self.pruning_method == "pct":
                local_prune_vals = get_filter_quantiles(
                    self.filter_source.f_vals[self.domain]
                )
                self._prune_vals = np.zeros_like(self.filter_source.f_vals)
                self._prune_vals[self.domain] = local_prune_vals
        return self._prune_vals

    @property
    def pruning_predicate(self):
        if self._pruning_predicate is None:
            prune_vals = self.prune_vals
            pruning_threshold = self.pruning_threshold
            self._pruning_predicate = LocalFunctionValuePruningPredicate(
                prune_vals, pruning_threshold, self.domain
            )
        return self._pruning_predicate


## implementation functions


# no need to do fancy compilation
def partition_filter_range_rng(f: np.ndarray, T: int) -> np.ndarray:
    """Return the boundary points of a partition of the range of f into T
    subintervals of equal length."""
    fmin = np.min(f)
    fmax = np.max(f)
    boundary_points = np.linspace(fmin, fmax, T + 1, dtype=np.float32)
    boundary_points[-1] = np.nextafter(boundary_points[-1], np.float32(np.inf))

    return boundary_points


# everything is vectorized so also no need to do any fancy compilation
def partition_filter_range_uni(f: np.ndarray, T: int) -> np.ndarray:
    """Return the boundary points of a partition of the range of f into T
    subintervals containing equal numbers of unique function values.

    When there are k < T unique values of f, only the first k intervals will
    contain function values, and the remainder of the intervals will have inf as
    a boundary.
    """
    f_uni = np.unique(f)
    n_unique = len(f_uni)
    idx_length = math.ceil(n_unique / T)
    boundary_points = np.full(T + 1, fill_value=np.inf, dtype=np.float32)

    # in most cases, this fills in the first T entries; if n_unique < T it fills
    # in the first n_unique entries
    boundary_indices = range(0, n_unique, idx_length)
    boundary_points[: len(boundary_indices)] = f_uni[boundary_indices]

    # this takes care of the upper bound, at index T or n_unique
    boundary_points[min(T, n_unique)] = np.nextafter(f_uni[-1], np.float32(np.inf))

    return boundary_points


@cython.boundscheck(False)
@cython.wraparound(False)
def partition_filter_domain(
    f: cython.float[::1], filter_partition: cython.float[::1]
) -> np.ndarray:
    """Produces a partition of the domain of f according to the given partition
    of the range."""

    N: cython.Py_ssize_t = len(f)
    partition = np.empty(N, dtype=np.int32)
    partition_view = cython.declare(int32_t[::1], partition)
    T: cython.Py_ssize_t = len(filter_partition) - 1
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    for i in range(N):
        for j in range(T):
            # bounds: i < N = len(f)
            # bounds: j + 1 < T + 1 = len(filter_partition)
            if f[i] < filter_partition[j + 1]:
                # bounds: i < N = len(partition)
                partition_view[i] = j
                break

    return partition


# I think what xshop does for quantiles is just get the indices for a uniform
# partition into 100 subintervals. probably faster, and good enough for Mapper.
@cython.wraparound(False)
@cython.cdivision(True)
def get_filter_quantiles(f: cython.float[::1]) -> np.ndarray:
    """Computes the quantiles of filter function values: q[i] = proportion of
    values of f that are strictly less than f[i]."""
    N: cython.Py_ssize_t = len(f)
    quantiles = np.zeros(N, dtype=np.float32)
    quantiles_view = cython.declare(cython.float[::1], quantiles)
    f_sort_idx: cython.Py_ssize_t[::1] = np.argsort(f)
    n_lesser_values: cython.float = 0
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    for i in range(1, N):
        j = f_sort_idx[i]
        prev_j = f_sort_idx[i - 1]
        if f[j] > f[prev_j]:
            n_lesser_values = i
        # f[j] is strictly greater than n_lesser_values other values
        quantiles_view[j] = n_lesser_values / N

    return quantiles

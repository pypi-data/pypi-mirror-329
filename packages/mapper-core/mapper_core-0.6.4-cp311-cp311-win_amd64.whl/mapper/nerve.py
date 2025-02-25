# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++

from typing import List, Tuple

import cython
import numpy as np
from cython.cimports.libc.stdint import int32_t
from cython.cimports.libcpp.map import map as stdmap
from cython.cimports.libcpp.pair import pair
from cython.cimports.libcpp.set import set as stdset
from cython.cimports.libcpp.vector import vector

bool_like = cython.fused_type(cython.char, cython.integral)


@cython.boundscheck(False)
@cython.wraparound(False)
def partition_set_sizes(partition: int32_t[::1]) -> np.ndarray:
    """Returns the size of each set in a partition."""
    sizes = np.zeros(np.max(partition) + 1, dtype=np.int32)
    sizes_view = cython.declare(int32_t[::1], sizes)
    # bounds: i < max(partition) + 1 = len(sizes)
    # we check for negative indices and ignore them
    for i in partition:
        if i >= 0:
            sizes_view[i] += 1
    return sizes


# TODO: make calls to numpy constructors via the C API
@cython.boundscheck(False)
@cython.wraparound(False)
def partition_vec_to_cover(partition_vec: cython.integral[::1]) -> List[np.ndarray]:
    """Converts a length-N vector whose entries give the partition set for each
    point into a list of lists."""
    # we assume that partitions are indexed contiguously beginning from 0,
    # although nothing breaks if a partition index is missing, just empty
    # arrays in the output. negative-indexed partitions are ignored

    # using stable sort means that the indices will already be sorted in each partition
    sort_idx: cython.Py_ssize_t[::1] = np.argsort(partition_vec, kind="stable")

    n_elts: cython.Py_ssize_t = partition_vec.shape[0]
    n_sets: cython.Py_ssize_t = partition_vec[sort_idx[n_elts - 1]] + 1

    cover = np.empty(n_sets, dtype=object)

    # we start outputting partitions indexed from 0
    current_partition: int32_t = 0
    last_idx: cython.Py_ssize_t
    i: cython.Py_ssize_t
    start_i: cython.Py_ssize_t

    # move past any negative elements
    for start_i in range(n_elts):
        # bounds: len(sort_idx) = n_elts
        # sort_idx has all in-bounds indices for partition_vec
        val = partition_vec[sort_idx[start_i]]
        if val >= 0:
            last_idx = start_i
            break

    for i in range(last_idx, n_elts):
        # bounds: len(sort_idx) = n_elts
        # sort_idx has all in-bounds indices for partition_vec
        val = partition_vec[sort_idx[i]]
        if val != current_partition:
            # we found the end of the current partition, so add it to the list
            # bounds: current_partition is always between 0 and max(partition_vec)
            # cover is constructed to have max(partition_vec) + 1 elements
            # last_idx <= i and i is always less than n_elts
            cover[current_partition] = np.array(sort_idx[last_idx:i], dtype=np.int32)
            # now add empty sets for any missing sequential values
            for p in range(current_partition + 1, val):
                # bounds: p is always less than max(partition_vec)
                cover[p] = np.empty(0, dtype=np.int32)
            current_partition = val
            last_idx = i
    # bounds: current_partition = val in last iteration, comes from partition_vec
    # bounds: last_idx < n_elts
    cover[current_partition] = np.array(sort_idx[last_idx:], dtype=np.int32)

    return cover.tolist()


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def weighted_partition_graph_edge_list_csr(
    neighbors: int32_t[::1],
    weights: cython.float[:],
    neighborhood_boundaries: int32_t[::1],
    edge_ranks: int32_t[:],
    mask: bool_like[:],
    max_rank: int32_t,
    partition_vec: np.ndarray,
    cover: List[np.ndarray],
    normalize_weights: bool = True,
    normalize_power: cython.float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Edge-based approach to producing a partition graph. Requires both the
    membership vector and the list of sets representation. Assumes the graph and
    mask are symmetric."""

    # this is an attempt to be more clever, requiring more effort for
    # correctness.  it works by using the neighbors array as indices into the
    # partition membership vector, replacing each neighbor graph node index with
    # the index of a partition set. then, it pulls out the rows of this array
    # corresponding with each set in the partition, deduplicates them, and
    # extracts the edge pairs.

    should_normalize_weights: cython.char = normalize_weights

    partition_neighbors = partition_vec[neighbors].astype(np.int32)
    partition_neighbors_view: int32_t[::1] = partition_neighbors

    edge_list: vector[pair[int32_t, int32_t]] = vector[pair[int32_t, int32_t]]()
    edge_weights: vector[cython.float] = vector[cython.float]()

    u_nbrs: stdmap[int32_t, cython.float] = stdmap[int32_t, cython.float]()

    n_cover_sets: cython.Py_ssize_t = len(cover)
    udx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    i: cython.Py_ssize_t
    vdx: int32_t
    udx: int32_t
    u_size: cython.float
    v_size: cython.float
    edge_weight: cython.float

    cover_sizes: vector[int32_t] = vector[int32_t]()

    if should_normalize_weights:
        for udx in range(n_cover_sets):
            # bounds: udx < n_cover_sets = len(cover)
            cover_sizes.push_back(cover[udx].shape[0])

    for udx in range(n_cover_sets):
        # bounds: udx < n_cover_sets = len(cover)
        u = cover[udx]
        u_view = cython.declare(int32_t[::1], u)
        u_nbrs.clear()

        # accumulate the weights for all neighboring partitions of u
        j = 0
        for i in u_view:
            # bounds: assumption is that elements of u are indices of nodes
            for j in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
                # bounds: len(mask) == max(neighborhood_boundaries)
                # bounds: len(edge_ranks) == max(neighborhood_boundaries)
                if mask[j] and (edge_ranks[j] < max_rank):
                    # bounds: len(partition_neighbors) == len(neighbors)
                    # == max(neighborhood_boundaries)
                    u_nbr = partition_neighbors_view[j]
                    # bounds: len(weights) == len(neighbors)
                    # == max(neighborhood_boundaries)
                    u_nbr_weight = weights[j]
                    if u_nbrs.count(u_nbr) == 0:
                        # bounds: u_nbrs is a map
                        u_nbrs[u_nbr] = u_nbr_weight
                    else:
                        u_nbrs[u_nbr] += u_nbr_weight

        # convert these partitions into the edge list/weights
        for entry in u_nbrs:
            # this always fails if vdx = -1
            vdx = entry.first
            if vdx > udx:
                edge_weight = entry.second
                if should_normalize_weights:
                    # bounds: udx < n_cover_sets == len(cover_sizes)
                    u_size = cover_sizes[udx]
                    # bounds: vdx < max(partition_vec) + 1 == n_cover_sets
                    # == len(cover_sizes)
                    v_size = cover_sizes[vdx]
                    edge_weight = edge_weight / ((u_size * v_size) ** normalize_power)
                edge_list.push_back(pair[int32_t, int32_t](udx, vdx))
                edge_weights.push_back(edge_weight)

    # reorganize into arrays
    edge_array = np.empty((edge_list.size(), 2), dtype=np.int32)
    weights_array = np.empty(edge_list.size(), dtype=np.float32)
    edge_array_view = cython.declare(int32_t[:, ::1], edge_array)
    weights_array_view = cython.declare(cython.float[::1], weights_array)

    for i in range(edge_list.size()):
        # bounds: i < edge_list.size() == edge_array.shape[0] == len(weights_array)
        edge_array_view[i, 0] = edge_list[i].first
        edge_array_view[i, 1] = edge_list[i].second
        weights_array_view[i] = edge_weights[i]

    return edge_array, weights_array
    # return edge_list, edge_weights


@cython.boundscheck(False)
@cython.wraparound(False)
def partition_graph_edge_list_csr(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    edge_ranks: int32_t[::1],
    mask: bool_like[::1],
    max_rank: int32_t,
    partition_vec: np.ndarray,
    cover: List[np.ndarray],
) -> List[Tuple[int, int]]:
    """Edge-based approach to producing a partition graph. Requires both the
    membership vector and the list of sets representation. Assumes the graph and
    mask are symmetric."""

    partition_neighbors = partition_vec[neighbors].astype(np.int32)
    partition_neighbors_view = cython.declare(int32_t[::1], partition_neighbors)

    edge_list: vector[pair[int32_t, int32_t]] = vector[pair[int32_t, int32_t]]()

    u_nbrs: stdset[int32_t] = stdset[int32_t]()

    n_cover_sets: cython.Py_ssize_t = len(cover)
    udx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    i: cython.Py_ssize_t
    vdx: int32_t
    udx: int32_t

    for udx in range(n_cover_sets):
        u = cover[udx]
        u_view = cython.declare(int32_t[::1], u)
        u_nbrs.clear()

        # accumulate the weights for all neighboring partitions of u
        j = 0
        for i in u_view:
            for j in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
                if mask[j] and (edge_ranks[j] < max_rank):
                    u_nbr = partition_neighbors_view[j]
                    u_nbrs.insert(u_nbr)

        # convert these partitions into the edge list/weights
        for vdx in u_nbrs:
            # this always fails if vdx = -1
            if vdx > udx:
                edge_list.push_back(pair[int32_t, int32_t](udx, vdx))

    return edge_list

# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++
"""Functions that work with the raw data structures for neighborhood graphs."""

from typing import Callable, List, Optional, Tuple, Union

import cython
import numpy as np
import pynndescent
import scipy.sparse
from cython.cimports.libc.math import INFINITY, exp, fabs, log2
from cython.cimports.libc.stdint import int32_t

# The main data structure here is a triple of arrays (neighbors, distances,
# n_neighbors), where
# - neighbors is an N x M array of int32 indices,
# - distances is an N x M array of floats, and
# - n_neighbors is a length-N array of indices.

# The idea is that neighbors[i,:] contains the indices of up to M
# neighbors of data point i, with the exact number stored given by k =
# n_neighbors[i]. distances[i,:k] then contains the distance from i to the
# corresponding nearest neighbors. The uninitialized entries in neighbors[i,:]
# (i.e., those after k) should all be equal to -1, and the corresponding entries
# in distances[i,:] should be inf.

# This is pretty similar to a compressed sparse row representation of the
# adjacency matrix, but instead of storing the start index for each row, we
# assume every row has a number of nonzero entries bounded above by M and
# reserve exactly that amount of space for it. (Specifically, distances is the
# array of values, neighbors is the array of column indices, and the array of
# row indices is implicit, with n_neighbors playing a similar role of
# identifying which entries in the values array to ignore for each row. The
# n_neighbors array is not strictly needed because we can use sentinel values
# for indices (-1) and distances (inf) to signal that these values should not be
# considered.)

# Once the edge truncation is done, this is translated to CSR format.
# structure: 1-d arrays neighbors, distances, edge_ranks (length 2 * |E|),
# neighborhood_boundaries (length |V| + 1), storing a symmetric adjacency matrix
# in CSR format. this means that the neighbors of node i are stored in
# neighbors[neighborhood_boundaries[i]:neighborhood_boundaries[i+1]], and their
# corresponding distances in
# distances[neighborhood_boundaries[i]:neighborhood_boundaries[i+1]]. every edge
# is stored in both directions, so if j is a neighbor of i, then i is a neighbor
# of j, and they have the same distances and edge ranks.

# we ensure every node has degree at least min_nbrs by never removing its
# min_nbrs nearest neighbors while processing. concretely, this is done by only
# applying the M-symmetrization step to the edges of rank min_nbrs through M.
# this leaves us with some edges going in only one direction. at this point we
# convert from the 2d arrays to a CSR format that allows arbitrary node degrees,
# and make the output edge-symmetric.

# Normalization still happens with the out-neighbors of each node, as is done by UMAP.

# the CSR format is flexible enough that we could go all in on the umap graph
# construction, and go from distances to weights with the filtration going the
# opposite direction. not sure if the product t-norm symmetrization makes sense
# for, like, doing filtered connected components.

# The main processing pipeline is as follows:
# 1. Extract the (approximate) M nearest neighbors of each data point

# 2. Symmetrize these neighborhood lists by restricting to mutual nearest
#    neighbors and removing the neighbors of rank > K that aren't required by
#    symmetry, but keeping the first `min_nbrs` neighbors for each node. These
#    neighborhoods may still be asymmetrical, but they are more symmetrical than before.
# 3. Compute normalized local distances for the neighborhood of each point. This
#    makes the distance array asymmetric.
# 4. Rank the edges according to these asymmetric distances.
# 5. Symmetrize the neighbors, distances, and ranks, storing the output in a
#    CSR adjacency matrix format.

# The CSR format could also be used for the output partition graph, instead of
# an edge list. Not sure if that would be an improvement.

# TODO: break this into smaller modules

MAX_INT = 2**31 - 1


def get_neighbors(
    X: Union[np.ndarray, scipy.sparse.csr_array, scipy.sparse.csr_matrix],
    M: int,
    metric: Union[str, Callable] = "euclidean",
    n_iters: Optional[int] = None,
    init_graph: Optional[np.ndarray] = None,
    init_dist: Optional[np.ndarray] = None,
    seed: Optional[int] = None,
    n_jobs: Optional[int] = -1,
) -> Tuple[np.ndarray, np.ndarray]:
    """Get the M nearest neighbors and their corresponding distances for each
    data point in X."""
    if init_graph is not None:
        init_graph = fill_init_graph(init_graph, M)
        if init_dist is not None:
            init_dist = fill_init_dist(init_dist, M)
    # pynndescent only supports csr_matrix for some reason
    if isinstance(X, scipy.sparse.csr_array):
        X = scipy.sparse.csr_matrix(X)
    index = pynndescent.NNDescent(
        X,
        metric=metric,
        n_neighbors=M + 1,
        n_iters=n_iters,
        random_state=seed,
        n_jobs=n_jobs,
        init_graph=init_graph,
        init_dist=init_dist,
    )
    # M+1 because pynndescent counts a point as its own neighbor
    # TODO: when are parallelization and other optimizations a performance win?

    neighbors, distances = index.neighbor_graph
    distances = distances.astype(np.float32)

    # Slicing out the unwanted self-neighbor in column 0 disrupts memory
    # contiguity, so we need np.ascontiguousarray() to return to C-contiguous
    # mem layout.

    move_self_edges_inplace(neighbors, distances)

    # TODO: it's probably a good idea to quotient out identical points if
    # possible, particularly for the Hamming metric

    neighbors = np.ascontiguousarray(neighbors[:, 1:].astype(np.int32))
    distances = np.ascontiguousarray(distances[:, 1:].astype(np.float32))

    return neighbors, distances


# Not much need to Cythonize this
def merge_knn_graphs(
    neighbors: List[np.ndarray], distances: List[np.ndarray], node_ids: List[np.ndarray]
) -> Tuple[np.ndarray, np.ndarray]:
    """Combines a collection of disjoint KNN graphs into one."""
    n_data_points = sum(u.shape[0] for u in node_ids)
    out_nbrs = np.empty_like(neighbors[0], shape=(n_data_points, neighbors[0].shape[1]))
    out_dists = np.empty_like(
        distances[0], shape=(n_data_points, distances[0].shape[1])
    )
    for nbrs, dists, nodes in zip(neighbors, distances, node_ids):
        out_nbrs[nodes, :] = nodes[nbrs]
        out_dists[nodes, :] = dists

    return out_nbrs, out_dists


@cython.boundscheck(False)
@cython.wraparound(False)
def move_self_edges_inplace(
    neighbors: int32_t[:, ::1], distances: cython.float[:, ::1]
):
    """Move neighbor indices so a node's first neighbor is always itself."""
    N: cython.Py_ssize_t = neighbors.shape[0]
    n_nbrs: cython.Py_ssize_t = neighbors.shape[1]
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t

    for i in range(N):
        # bounds: i < N = neighbors.shape[0]
        if neighbors[i, 0] == i:
            continue
        else:
            for jdx in range(n_nbrs):
                # bounds: 0 <= i < N = neighbors.shape[0]
                # bounds: 0 <= jdx < n_nbrs = neighbors.shape[1]
                if neighbors[i, jdx] == i:
                    # bounds: the slice is valid even if neighbors.shape[0] = 1
                    neighbors[i, 1 : jdx + 1] = neighbors[i, 0:jdx]
                    distances[i, 1 : jdx + 1] = distances[i, 0:jdx]
                    neighbors[i, 0] = i
                    distances[i, 0] = 0


# TODO: are these functions even necessary/helpful?
@cython.boundscheck(False)
@cython.wraparound(False)
def fill_init_graph(init_graph: int32_t[:, ::1], M: int32_t):
    """Converts an N x K neighbor array to an N x (M+1) array."""
    N: cython.Py_ssize_t = init_graph.shape[0]
    K: cython.Py_ssize_t = init_graph.shape[1]
    new_graph = np.empty(shape=(N, M + 1), dtype=init_graph.dtype)
    new_graph_view = cython.declare(int32_t[:, ::1], new_graph)
    i: cython.Py_ssize_t

    K = min(K, M)

    for i in range(N):
        # bounds: 0 <= i < N = new_graph.shape[0]
        new_graph_view[i, 0] = i
        # bounds: K <= M from above, so K + 1 <= M + 1 = new_graph.shape[1]
        new_graph_view[i, 1 : K + 1] = init_graph[i, :]
        new_graph_view[i, K + 1 :] = -1
    return new_graph


@cython.boundscheck(False)
@cython.wraparound(False)
def fill_init_dist(init_dist: cython.float[:, ::1], M: int32_t):
    """Converts an N x K distance array to an N x (M+1) array."""
    N: cython.Py_ssize_t = init_dist.shape[0]
    K: cython.Py_ssize_t = init_dist.shape[1]
    new_dist = np.empty(shape=(N, M + 1), dtype=init_dist.dtype)
    new_dist_view = cython.declare(cython.float[:, ::1], new_dist)
    i: cython.Py_ssize_t

    K = min(K, M)

    for i in range(N):
        # bounds: 0 <= i < N = new_dist.shape[0]
        new_dist_view[i, 0] = 0
        # bounds: K <= M by construction, so K + 1 <= M + 1 = new_dist.shape[1]
        new_dist_view[i, 1 : K + 1] = init_dist[i, :]
        # pynndescent ignores the other entries but requires the shape to match
        # new_graph[i, K + 1 :] = 0
    return new_dist


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cfunc
def compress_nbhds_inplace(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
):
    """Moves uninitialized neighbors (those with value -1) to the end of the
    list for each entry. Of course does the same to distances, and updates
    n_neighbors to the correct value."""
    N: cython.Py_ssize_t = neighbors.shape[0]
    M: cython.Py_ssize_t = neighbors.shape[1]
    tmp_nbr = cython.declare(int32_t[::1], np.empty(M, dtype=np.int32))
    tmp_dist = cython.declare(cython.float[::1], np.empty(M, dtype=np.float32))
    i: cython.Py_ssize_t

    for i in range(N):
        new_jdx = 0
        # bounds: i < N = neighbors.shape[0] = len(n_neighbors)
        for jdx in range(n_neighbors[i]):
            # bounds: i < N = neighbors.shape[0]
            # bounds: jdx < n_neighbors[i] <= neighbors.shape[1]
            j = neighbors[i, jdx]
            if j != -1:
                # bounds: new_jdx starts at 0 and increments at most once
                # for every iteration of the inner loop
                # therefore new_jdx < n_neighbors[i] <= neighbors.shape[1]
                # = len(tmp_nbr) = len(tmp_dist)
                tmp_nbr[new_jdx] = j
                tmp_dist[new_jdx] = distances[i, jdx]
                new_jdx += 1
        # bounds: i < N
        # bounds: new_jdx < neighbors.shape[1]
        neighbors[i, :new_jdx] = tmp_nbr[:new_jdx]
        distances[i, :new_jdx] = tmp_dist[:new_jdx]
        neighbors[i, new_jdx:] = -1
        distances[i, new_jdx:] = INFINITY
        n_neighbors[i] = new_jdx


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def get_directed_edge_ranks(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
):
    """Get a rank for each directed edge, taking into account duplicate
    distances. Assumes distances are sorted in increasing order."""
    N: cython.Py_ssize_t = neighbors.shape[0]
    edge_ranks = np.full_like(neighbors, MAX_INT, dtype=np.int32)
    edge_ranks_view = cython.declare(int32_t[:, ::1], edge_ranks)
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    r: int32_t

    for i in range(N):
        # bounds: i < N = neighbors.shape[0] = len(n_neighbors)
        if n_neighbors[i] <= 0:
            continue
        r = 0
        for jdx in range(n_neighbors[i] - 1):
            # bounds: i < N = edge_ranks.shape[0]
            # bounds: 0 <= jdx < n_neighbors[i] - 1 < neighbors.shape[1]]
            edge_ranks_view[i, jdx] = r
            # bounds: i < N = distances.shape[0]
            # bounds: 0 <= jdx < n_neighbors[i] - 1 < distances.shape[1]]
            if distances[i, jdx + 1] > distances[i, jdx]:
                r += 1
        # bounds: n_neighbors[i] > 0 from check at the beginning of the loop
        # n_neighbors[i] <= edge_ranks.shape[1]
        edge_ranks_view[i, n_neighbors[i] - 1] = r
    return edge_ranks


# TODO: not sure we need this function any more since symmetrization happens in
# the CSRification step.
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cfunc
def symmetrize_edge_ranks(
    neighbors: int32_t[:, ::1],
    edge_ranks: int32_t[:, ::1],
    n_neighbors: int32_t[::1],
) -> int32_t[:, ::1]:
    """Symmetrize an array of edge ranks by taking the minimum in each direction."""
    N: cython.Py_ssize_t = neighbors.shape[0]
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t

    for i in range(N):
        for jdx in range(n_neighbors[i]):
            # bounds: i < N = neighbors.shape[0]
            # bounds: 0 <= jdx < n_neighbors[i] < neighbors.shape[1]]
            j = neighbors[i, jdx]
            # since jdx < n_neighbors[i], we know j != -1
            # and j is a valid node index
            for idx in range(n_neighbors[j]):
                # bounds: j is a valid node index
                # idx < n_neighbors[j] <= neighbors.shape[1]
                if neighbors[j, idx] == i:
                    # bounds: edge_ranks.shape = neighbors.shape
                    rank = min(edge_ranks[i, jdx], edge_ranks[j, idx])
                    edge_ranks[i, jdx] = rank
                    edge_ranks[j, idx] = rank
                    break
    return edge_ranks


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def get_edge_ranks_distances(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
) -> int32_t[:, ::1]:
    """Get a rank for each undirected edge by taking the minimum rank in each
    direction. Assumes edges are sorted by increasing distance."""

    edge_ranks = get_directed_edge_ranks(neighbors, distances, n_neighbors)
    symmetrize_edge_ranks(neighbors, edge_ranks, n_neighbors)
    return edge_ranks


@cython.boundscheck(False)
@cython.wraparound(False)
def symmetrize_neighbors(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    K: int32_t,
    min_nbrs: int32_t,
):
    """Symmetrize the neighborhood graph by removing any non-mutual M-nearest
    neighbors of rank > min_nbrs and then removing all links where both
    directions are of rank > K.

    This version does what the xshop implementation actually does.
    """

    N: cython.Py_ssize_t = neighbors.shape[0]
    M: cython.Py_ssize_t = neighbors.shape[1]

    K_neighbors = np.array(neighbors.copy())
    K_distances = np.array(distances.copy())
    n_neighbors = np.full(N, fill_value=M, dtype=np.int32)
    K_neighbors_view = cython.declare(int32_t[:, ::1], K_neighbors)
    K_distances_view = cython.declare(cython.float[:, ::1], K_distances)
    n_neighbors_view = cython.declare(int32_t[::1], n_neighbors)

    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    idx: cython.Py_ssize_t

    # first remove all edges of rank > min_nbrs whose reverse edge does not exist.
    # TODO: use a rank that takes into account repeated distances
    for i in range(N):
        # always keep the first min_nbrs neighbors
        for jdx in range(min_nbrs, M):
            # bounds: i < N = neighbors.shape[0]
            # bounds: 0 <= min_nbrs <= N < M = neighbors.shape[1]
            j = neighbors[i, jdx]
            # j is a valid index < N
            # check if i is a neighbor of j
            for idx in range(M):
                # bounds: 0 <= j < N
                # bounds: idx < M = K_neighbors.shape[1]
                if K_neighbors_view[j, idx] == i:
                    break
            else:
                # bounds: 0 <= i < N
                # bounds: 0 <= min_nbrs <= jdx < M
                K_neighbors_view[i, jdx] = -1
                K_distances_view[i, jdx] = INFINITY

    # after this, all -1s will be at the end of the row
    # and n_neighbors has the location of the last valid entry
    compress_nbhds_inplace(K_neighbors_view, K_distances_view, n_neighbors_view)

    # now remove any neighbors after rank K unless their reverse neighbor link
    # is of rank < K
    for i in range(N):
        for jdx in range(K, n_neighbors_view[i]):
            # bounds: 0 <= i < N = K_neighbors.shape[0]
            # bounds: 0 <= K <= jdx < n_neighbors[i] <= K_neighbors.shape[1]
            j = K_neighbors_view[i, jdx]
            if j >= 0:
                for idx in range(K):
                    # bounds: j >= 0 and is a valid index
                    # bounds: 0 <= idx < K <= K_neighbors.shape[1]
                    if K_neighbors_view[j, idx] == i:
                        break
                else:
                    # bounds: 0 <= i < N = K_neighbors.shape[0]
                    # bounds: 0 <= K <= jdx < n_neighbors[i] <= K_neighbors.shape[1]
                    K_neighbors_view[i, jdx] = -1
                    K_distances_view[i, jdx] = INFINITY

    compress_nbhds_inplace(K_neighbors_view, K_distances_view, n_neighbors_view)

    return K_neighbors, K_distances, n_neighbors


@cython.profile(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cfunc
@cython.cdivision(True)  # prevents checking for division by zero
@cython.exceptval(check=False)  # does not throw exceptions, so caller shouldn't check
def neighborhood_sum(distances: cython.float[::1], sigma: cython.float) -> cython.float:
    acc: cython.float = 0
    n: cython.Py_ssize_t = distances.shape[0]
    i: cython.Py_ssize_t
    for i in range(n):
        # bounds: 0 <= i < n = distances.shape[0]
        acc += exp(-distances[i] / sigma)
    return acc


@cython.profile(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def get_sigma(
    distances: cython.float[::1], abs_tol: cython.float = 1e-6, maxiter: int32_t = 20
) -> cython.float:
    """Solve Σ_j exp(-distances/sigma) = log_2(len(distances))."""

    n_neighbors = distances.shape[0]

    # edge cases:
    # if zero neighbors, just let sigma=1 (it doesn't matter)
    if n_neighbors == 0:
        return 1.0
    # if all distances are zero, the total is constant, and it doesn't matter
    # what sigma is
    for i in range(n_neighbors):
        # bounds: i < n_neighbors = distances.shape[0]
        if distances[i] != 0:
            break
    else:
        return 1.0
    # if one neighbor, return the distance so the normalized distance is 1.
    # this seems ok in practice?
    if n_neighbors == 1:
        # bounds: 0 < 1 = n_neighbors = distances.shape[0]
        return distances[0]

    target: cython.float = log2(n_neighbors)

    sigma: cython.float
    total: cython.float
    sigma_min: cython.float
    sigma_max: cython.float
    err: cython.float

    # find upper and lower bounds on sigma
    # lower bound
    sigma = 1.0
    total = neighborhood_sum(distances, sigma)
    for _ in range(maxiter):
        if total >= target:
            break
        sigma = sigma * 2
        total = neighborhood_sum(distances, sigma)
    else:
        # we weren't able to find a sigma that brought the sum above the
        # target, so just use the one that (hopefully) gets closest.
        return sigma
    sigma_min = sigma

    # upper bound
    sigma = 1.0
    total = neighborhood_sum(distances, sigma)
    for _ in range(maxiter):
        if total <= target:
            break
        sigma = sigma / 2
        total = neighborhood_sum(distances, sigma)
    else:
        # failed to find a sigma that brought the sum below the target, so
        # use the one that gets closest.
        return sigma
    sigma_max = sigma

    # binary search for sigma
    # this works because neighborhood_sum is monotone
    sigma = (sigma_min + sigma_max) / 2
    total = neighborhood_sum(distances, sigma)
    err = fabs(total - target)
    for _ in range(maxiter):
        if err <= abs_tol:
            break
        if total > target:
            sigma_min = sigma
        else:
            sigma_max = sigma
        sigma = (sigma_min + sigma_max) / 2
        total = neighborhood_sum(distances, sigma)

    if sigma == 0:
        return 1

    return sigma


# TODO: this is the slowest part of the graph computation (besides pynndescent).
# would doing it in-place or parallel make it faster?
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def get_sigmas(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
    abs_tol: cython.float = 1e-6,
    maxiter: int32_t = 20,
) -> cython.float[::1]:
    """Compute normalizing factors for neighborhood distances.

    For each point i, solves Σ_j exp(-d(i,j)/sigma) = log_2(K), where j ranges
    over the K neighbors of i."""

    N: cython.Py_ssize_t = neighbors.shape[0]
    sigmas = cython.declare(cython.float[::1], np.empty(N, dtype=np.float32))
    for i in range(N):
        # bounds: 0 <=i< N = distances.shape[0] = sigmas.shape[0] = n_neighbors.shape[0]
        sigmas[i] = get_sigma(distances[i, : n_neighbors[i]], abs_tol, maxiter)
    return sigmas


def normalize_distances(
    neighbors: np.ndarray,
    distances: np.ndarray,
    n_neighbors: np.ndarray,
) -> np.ndarray:
    """Normalizes the distances from each node i to its neighbors by scaling
    them uniformly so that Σ_j exp(-d_ij) = log_2(n_neighbors[i]).

    This results in different values for d_ij and d_ji, and so these will
    typically be symmetrized later."""
    # TODO: in-place implementation?
    sigmas = np.asarray(
        get_sigmas(neighbors, distances, n_neighbors, abs_tol=1e-6, maxiter=20)
    )
    nbhd_distances = distances / sigmas.reshape((-1, 1))
    return nbhd_distances


# TODO: clean up the symmetrization process. there's a lot of repeated work
@cython.boundscheck(False)
@cython.wraparound(False)
def to_symmetric_csr(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
):
    """Converts a (not necessarily symmetric) graph in KNN format to a symmetric
    graph in CSR format. Preserves both distances if an edge exists in both
    directions, and otherwise duplicates the single distance for the edge.
    Assumes input edges are sorted by desired rank.

    Returns:
        csr_neighbors: an int32 array of length (number of undirected edges) * 2
        containing the neighbors of each node.

        csr_distances: a float32 array of length (number of undirected edges) *
        2 containing the length of each edge.

        csr_neighborhood_boundaries: an int32 array of length N + 1 whose ith
        entry is the index in csr_neighbors and csr_distances where the data for
        neighbors of node i starts. The last entry is len(csr_neighbors).

        edge_ranks: an int32 array of the same shape as csr_neighbors giving the
        symmetrized rank of each edge.
    """

    # TODO: what if there are repeated distances/ranks?

    ## assume edges are sorted by distance rank
    N: cython.Py_ssize_t = neighbors.shape[0]

    edge_ranks: int32_t[:, ::1] = get_edge_ranks_distances(
        neighbors, distances, n_neighbors
    )

    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    idx: cython.Py_ssize_t

    # get total number of edges to allocate for each node
    csr_n_neighbors = cython.declare(int32_t[::1], n_neighbors.copy())
    for i in range(N):
        for jdx in range(n_neighbors[i]):
            j = neighbors[i, jdx]
            for idx in range(n_neighbors[j]):
                if neighbors[j, idx] == i:
                    break
            else:
                csr_n_neighbors[j] += 1

    # this is basically just
    # csr_neighborhood_boundaries = cumsum(csr_n_neighbors) (with a 0 at the beginning)
    nbhd_boundaries_arr = np.empty(N + 1, dtype=np.int32)
    nbhd_boundaries = cython.declare(int32_t[::1], nbhd_boundaries_arr)
    nbhd_boundaries[0] = 0
    acc: int32_t = 0
    for i in range(1, N + 1):
        acc += csr_n_neighbors[i - 1]
        nbhd_boundaries[i] = acc

    # total number of edges
    edge_count: int32_t = nbhd_boundaries[N]
    # number of edges added to each neighborhood
    # INVARIANT: edges_added[i] < nbhd_boundaries[i+1] - nbhd_boundaries[i]
    # (this is just csr_n_neighbors[i])
    # edges_added[i] increases once for each edge coming out of i
    # (i.e. n_neighbors[i] times)
    # plus once for each time i additionally shows up as an out-neighbor of another node
    # this is exactly the difference between n_neighbors[i] and csr_n_neighbors[i]
    edges_added_arr = np.zeros((N,), dtype=np.int32)
    edges_added = cython.declare(int32_t[::1], edges_added_arr)

    # arrays to fill with data
    csr_neighbors_arr = np.empty((edge_count,), dtype=np.int32)
    csr_neighbors = cython.declare(int32_t[::1], csr_neighbors_arr)
    csr_distances_arr = np.empty((edge_count), dtype=np.float32)
    csr_distances = cython.declare(cython.float[::1], csr_distances_arr)

    csr_edge_ranks_arr = np.empty((edge_count,), dtype=np.int32)
    csr_edge_ranks = cython.declare(int32_t[::1], csr_edge_ranks_arr)

    csr_i_start: cython.Py_ssize_t = 0
    for i in range(N):
        # bounds: 0 <= i < N = nbhd_boundaries.shape[0] - 1
        csr_i_start = nbhd_boundaries[i]
        # bounds: 0 <= i < N = n_neighbors.shape[0]
        for jdx in range(n_neighbors[i]):
            j = neighbors[i, jdx]
            nbr_ix = edges_added[i]
            # bounds: by the invariant above csr_i_start + nbr_ix < nbhd_boundaries[i+1]
            # this is at most len(csr_neighbors) = len(csr_distances)
            csr_neighbors[csr_i_start + nbr_ix] = j
            csr_distances[csr_i_start + nbr_ix] = distances[i, jdx]
            edges_added[i] += 1

            # check if we need to add the reverse edge or if it already exists
            for idx in range(n_neighbors[j]):
                if neighbors[j, idx] == i:
                    break
            else:
                # if i not in neighbors[j, : n_neighbors[j]]:
                nbr_ix = edges_added[j]
                csr_j_start = nbhd_boundaries[j]
                # TODO: is this a good choice for the reverse distance?
                # bounds: from invariant above csr_j_start+nbr_ix < nbhd_boundaries[j+1]
                # this is at most len(csr_neighbors) = len(csr_distances)
                csr_neighbors[csr_j_start + nbr_ix] = i
                csr_distances[csr_j_start + nbr_ix] = distances[i, jdx]
                edges_added[j] += 1

    # compute symmetrized edge ranks
    # this could be done at the same time as the construction above.
    csr_jdx: cython.Py_ssize_t
    for i in range(N):
        for csr_jdx in range(nbhd_boundaries[i], nbhd_boundaries[i + 1]):
            # most of this is identifying if an edge has one or two source ranks
            # bounds: 0 <= csr_jdx < max(nbhd_boundaries) = len(csr_neighbors)
            j = csr_neighbors[csr_jdx]
            # bounds: 0 <= i < N = len(n_neighbors)
            for jdx in range(n_neighbors[i]):
                # bounds: 0 <= jdx < n_neighbors[i] <= neighbors.shape[0]
                if neighbors[i, jdx] == j:
                    break
            else:
                jdx = -1

            # bounds: j in neighbors[i, :n_neighbors[i]]
            # so 0 <= j < N
            for idx in range(n_neighbors[j]):
                # bounds: 0 <= idx < n_neighbors[i] <= neighbors.shape[0]
                if neighbors[j, idx] == i:
                    break
            else:
                idx = -1

            # bounds: 0 <= csr_jdx < max(nbhd_boundaries) = len(csr_edge_ranks)
            # bounds: edge_ranks.shape = neighbors.shape
            if idx == -1:
                # jdx >= 0
                csr_edge_ranks[csr_jdx] = edge_ranks[i, jdx]
            elif jdx == -1:
                # idx >= 0
                csr_edge_ranks[csr_jdx] = edge_ranks[j, idx]
            else:
                # idx and jdx are >= 0 here
                csr_edge_ranks[csr_jdx] = min(edge_ranks[j, idx], edge_ranks[i, jdx])

    return (
        csr_neighbors_arr,
        csr_distances_arr,
        nbhd_boundaries_arr,
        csr_edge_ranks_arr,
    )


@cython.boundscheck(False)
@cython.wraparound(False)
def symmetrize_distances(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
) -> np.ndarray:
    """Computes d_ij = (d_ij + d_ji)/2. If one edge does not exist, does
    nothing."""

    # TODO: try averaging with the maximum of d_ji if one direction doesn't exist
    # TODO: in-place implementation?
    N: cython.Py_ssize_t = neighbors.shape[0]
    sym_dist = cython.declare(cython.float[:, ::1], np.copy(distances))
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    idx: cython.Py_ssize_t
    dij: cython.float
    dji: cython.float
    d: cython.float

    for i in range(N):
        # bounds: 0 <= i < N = len(n_neighbors)
        for jdx in range(n_neighbors[i]):
            # bounds: 0 <= i < N = neighbors.shape[0]
            # bounds: 0 <= jdx < n_neighbors[i] <= neighbors.shape[1]
            j = neighbors[i, jdx]
            if i < j:
                # bounds: neighbors.shape = distances.shape
                dij = distances[i, jdx]
                # bounds: j is a valid index because jdx < n_neighbors[i]
                for idx in range(n_neighbors[j]):
                    # bounds: j is a valid index
                    # 0 <= idx < n_neighbors[j] <= neighbors.shape[0]
                    if neighbors[j, idx] == i:
                        # bounds: distances.shape = neighbors.shape
                        dji = distances[j, idx]
                        d = (dij + dji) / 2
                        # bounds: sym_dist.shape = distances.shape
                        sym_dist[i, jdx] = d
                        sym_dist[j, idx] = d
                        break
                # # if the reverse edge doesn't exist, average with
                # # the distance for the furthest neighbor
                # else:
                #     dji = distances[j, idx]
                #     d = (dij + dji) / 2
                #     sym_dist[i, jdx] = d
    return sym_dist


@cython.boundscheck(False)
@cython.wraparound(False)
def rerank_nbhds(
    neighbors: int32_t[:, ::1],
    distances: cython.float[:, ::1],
    n_neighbors: int32_t[::1],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Reorder the list of neighbors so that it is in increasing order of
    normalized distance."""
    # TODO: compute symmetric ranks?
    # TODO: in-place implementation?
    N: cython.Py_ssize_t = neighbors.shape[0]
    rerank_neighbors = cython.declare(
        int32_t[:, ::1], np.full_like(neighbors, fill_value=-1)
    )
    rerank_distances = cython.declare(
        cython.float[:, ::1], np.full_like(distances, fill_value=INFINITY)
    )
    rerank_n_neighbors = cython.declare(int32_t[::1], np.copy(n_neighbors))
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    # this assumes that all distances for nonexistent edges are infinity
    index_rank = cython.declare(
        cython.Py_ssize_t[:, ::1], np.argsort(distances, axis=1)
    )
    for i in range(N):
        # bounds: 0 <= i < N = n_neighbors.shape[0]
        for jdx in range(n_neighbors[i]):
            # bounds: 0 <= jdx < n_neighbors[i] <= distances.shape[1]
            # = rerank-distances.shape[1]
            rerank_distances[i, jdx] = distances[i, index_rank[i, jdx]]
            if rerank_distances[i, jdx] == INFINITY:
                rerank_n_neighbors[i] = jdx
                break
            rerank_neighbors[i, jdx] = neighbors[i, index_rank[i, jdx]]
    return rerank_neighbors, rerank_distances, rerank_n_neighbors


@cython.boundscheck(False)
@cython.wraparound(False)
def get_knn_edge_list(
    neighbors: int32_t[:, ::1],
) -> List[Tuple[np.int32, np.int32]]:
    """Compute lists of edges in a (directed) KNN graph as tuples."""
    edge_list = []
    N: cython.Py_ssize_t = neighbors.shape[0]
    M: cython.Py_ssize_t = neighbors.shape[1]
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    for i in range(N):
        for jdx in range(M):
            # bounds: 0 <= i < N = neighbors.shape[0]
            # bounds: 0 <= jdx < M = neighbors.shape[1]
            j = neighbors[i, jdx]
            edge_list.append((i, j))
    return edge_list

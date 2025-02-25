# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=True
# distutils: language = c++

from typing import Callable, Tuple

import cython
import numpy as np
from cython.cimports.libc.stdint import int32_t
from scipy.stats import entropy

from mapper.affinities import distances_to_affinities_slpi
from mapper.cluster_tree import ClusterNode
from mapper.flat_cluster import LocalClusterScoreFunction
from mapper.neighborgraph import NeighborGraph

bool_like = cython.fused_type(cython.char, cython.integral)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def modularity_change(
    neighbors: int32_t[::1],
    affinities: cython.float[:],
    neighborhood_boundaries: int32_t[::1],
    new_clusters: Tuple[np.ndarray, ...],
    total_weight: cython.float,
    r: cython.float = 0.0,
) -> Tuple[float, float]:
    """Computes the change in modularity score induced by splitting a cluster.

    Only the new clusters need to be provided; the old cluster is assumed to be
    their union.
    """
    n_nodes: cython.int = neighborhood_boundaries.shape[0] - 1
    partition_vec_arr = np.full(n_nodes, -1, dtype=np.int32)

    idx: int32_t
    for idx, u in enumerate(new_clusters):
        partition_vec_arr[u] = idx
    partition_vec: int32_t[::1] = partition_vec_arr

    # sum of edge weights for edges inside the original cluster
    old_in_community_weight: cython.double = 0.0
    # sum of edge weights for edges inside each new cluster
    new_in_community_weights: cython.double[::1] = np.zeros(
        len(new_clusters), dtype=np.float64
    )
    # sum of edge weights for edges with one end in each new cluster
    total_new_community_weights: cython.double[::1] = np.zeros(
        len(new_clusters), dtype=np.float64
    )
    total_old_community_weight: cython.double = 0.0

    if total_weight <= 0:
        return 0.0, 0.0

    total_weight += r * n_nodes

    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    partition_j: int32_t
    partition_i: int32_t
    cl_i: cython.Py_ssize_t
    for partition_i in range(len(new_clusters)):
        cluster: int32_t[:] = new_clusters[partition_i]
        for cl_i in range(cluster.shape[0]):
            i = cluster[cl_i]
            new_in_community_weights[partition_i] += r
            old_in_community_weight += r
            total_new_community_weights[partition_i] += r
            total_old_community_weight += r
            for jdx in range(
                neighborhood_boundaries[i], neighborhood_boundaries[i + 1]
            ):
                j = neighbors[jdx]
                partition_j = partition_vec[j]
                if partition_j == partition_i:
                    new_in_community_weights[partition_i] += affinities[jdx]
                if partition_j != -1:
                    old_in_community_weight += affinities[jdx]
                total_new_community_weights[partition_i] += affinities[jdx]
                total_old_community_weight += affinities[jdx]

    new_modularity_terms: cython.double = 0.0
    for i in range(new_in_community_weights.shape[0]):
        new_modularity_terms += (new_in_community_weights[i] / total_weight) - (
            total_new_community_weights[i] / total_weight
        ) ** 2

    old_modularity_term: cython.double = (
        old_in_community_weight / total_weight
        - (total_old_community_weight / total_weight) ** 2
    )

    modularity_diff: cython.double = new_modularity_terms - old_modularity_term

    return old_modularity_term, modularity_diff


@cython.boundscheck(False)
@cython.wraparound(False)
def masked_total_weight(
    neighbors: int32_t[::1],
    affinities: cython.float[:],
    neighborhood_boundaries: int32_t[::1],
    node_mask: bool_like[:],
) -> cython.float:
    n_nodes: cython.int = neighborhood_boundaries.shape[0] - 1
    total_weight: cython.double = 0.0
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    for i in range(n_nodes):
        if not node_mask[i]:
            continue
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            if node_mask[j]:
                total_weight += affinities[jdx]

    return total_weight


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def masked_modularity_change(
    neighbors: int32_t[::1],
    affinities: cython.float[:],
    neighborhood_boundaries: int32_t[::1],
    node_mask: bool_like[:],
    new_clusters: Tuple[np.ndarray, ...],
    total_weight: cython.float,
    r: cython.float = 0.0,
) -> Tuple[float, float]:
    """Computes the change in modularity score induced by splitting a cluster.

    Only the new clusters need to be provided; the old cluster is assumed to be
    their union.
    """
    n_nodes: cython.int = neighborhood_boundaries.shape[0] - 1
    cluster_membership_arr = np.full(n_nodes, -1, dtype=np.int32)

    idx: int32_t
    for idx, u in enumerate(new_clusters):
        cluster_membership_arr[u] = idx
    cluster_membership: int32_t[::1] = cluster_membership_arr

    total_weight += r * np.sum(node_mask)

    # sum of edge weights for edges inside the original cluster
    old_in_community_weight: cython.double = 0.0
    # sum of edge weights for edges inside each new cluster
    new_in_community_weights: cython.double[::1] = np.zeros(
        len(new_clusters), dtype=np.float64
    )
    # sum of edge weights for edges with one end in each new cluster
    total_new_community_weights: cython.double[::1] = np.zeros(
        len(new_clusters), dtype=np.float64
    )
    total_old_community_weight: cython.double = 0.0

    partition_i: cython.Py_ssize_t
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    cluster: int32_t[:]
    for partition_i in range(len(new_clusters)):
        cluster: int32_t[:] = new_clusters[partition_i]
        for cl_i in range(cluster.shape[0]):
            i = cluster[cl_i]
            new_in_community_weights[partition_i] += r
            old_in_community_weight += r
            total_new_community_weights[partition_i] += r
            total_old_community_weight += r
            if not node_mask[i]:
                continue
            for jdx in range(
                neighborhood_boundaries[i], neighborhood_boundaries[i + 1]
            ):
                j = neighbors[jdx]
                if not node_mask[j]:
                    continue
                if cluster_membership[j] == partition_i:
                    new_in_community_weights[partition_i] += affinities[jdx]
                if cluster_membership[j] != -1:
                    old_in_community_weight += affinities[jdx]
                total_new_community_weights[partition_i] += affinities[jdx]
                total_old_community_weight += affinities[jdx]

    new_modularity_terms: cython.double = 0.0
    for i in range(new_in_community_weights.shape[0]):
        new_modularity_terms += (new_in_community_weights[i] / total_weight) - (
            total_new_community_weights[i] / total_weight
        ) ** 2

    old_modularity_term: cython.double = (
        old_in_community_weight / total_weight
        - (total_old_community_weight / total_weight) ** 2
    )

    modularity_diff: cython.double = new_modularity_terms - old_modularity_term

    return old_modularity_term, modularity_diff


@cython.annotation_typing(False)
def sample_entropy(x: np.ndarray) -> float:
    """Entropy of the empirical distribution of a sample of a categorical variable.

    Ignores NaN values.
    """
    x = x[~np.isnan(x)]
    _, dist = np.unique(x, return_counts=True)
    return entropy(dist)


@cython.annotation_typing(False)
def scaled_sample_entropy(x: np.ndarray) -> float:
    """Entropy scaled by the number of samples."""
    return len(x) * sample_entropy(x)


@cython.annotation_typing(False)
def gini_impurity(x: np.ndarray) -> float:
    """Gini index of the empirical distribution of a sample of a categorical variable.

    Ignores NaN values.
    """
    x = x[~np.isnan(x)]
    _, dist = np.unique(x, return_counts=True)
    dist = dist / len(x)
    return np.sum(dist * (1 - dist))


@cython.annotation_typing(False)
def scaled_gini_impurity(x: np.ndarray) -> float:
    """Gini impurity scaled by the number of samples."""
    return len(x) * gini_impurity(x)


@cython.annotation_typing(False)
def make_local_score_fn(
    f: np.ndarray, arr_fn: Callable[[np.ndarray], float]
) -> LocalClusterScoreFunction:
    """Produce a cluster scoring function applying arr_fn to f on each cluster."""

    def local_score(node: ClusterNode) -> Tuple[float, float]:
        full_score = arr_fn(f[node.datapoints])
        if len(node.children) == 0:
            return full_score, 0
        split_scores = [arr_fn(f[c.datapoints]) for c in node.children]
        return full_score, sum(split_scores) - full_score

    return local_score


@cython.annotation_typing(False)
def make_local_entropy_score_fn(
    f: np.ndarray,
) -> LocalClusterScoreFunction:
    """Produce a scoring function computing the scaled entropy of f on each cluster."""
    return make_local_score_fn(f, scaled_sample_entropy)


@cython.annotation_typing(False)
def make_local_variance_score_fn(f: np.ndarray) -> LocalClusterScoreFunction:
    """Produce a scoring function computing the variance of f on each cluster."""
    return make_local_score_fn(f, np.var)


@cython.annotation_typing(False)
def make_local_score_threshold_fn(
    score_fn: LocalClusterScoreFunction, threshold: float
) -> LocalClusterScoreFunction:
    """Transform a scoring function to be equal to zero if it is below a threshold."""

    def local_score(node: ClusterNode) -> Tuple[float, float]:
        score, score_diff = score_fn(node)
        split_score = score + score_diff

        if score < threshold:
            score_diff = max(0, split_score)
            if score_diff < threshold:
                score_diff = 0
            score = 0
        elif split_score < threshold:
            score_diff = -score
        return score, score_diff

    return local_score


@cython.annotation_typing(False)
def make_local_negative_modularity_score_fn(
    graph: NeighborGraph, modularity_r: float = 0
) -> LocalClusterScoreFunction:
    """Produce a scoring function that computes modularity on the provided graph."""
    neighbors = graph.graph._neighbors
    distances = graph.graph._distances
    affinities = distances_to_affinities_slpi(distances)
    nbhd_boundaries = graph.graph._neighborhood_boundaries
    total_weight = np.sum(affinities)
    # TODO: use mask when it matters

    def local_modularity_score(node: ClusterNode) -> Tuple[float, float]:
        # TODO: change type
        new_clusters = tuple([c.datapoints for c in node.children])
        if len(new_clusters) > 0:
            modularity, modularity_diff = modularity_change(
                neighbors,
                affinities,
                nbhd_boundaries,
                new_clusters,
                total_weight,
                r=modularity_r,
            )
        else:
            modularity, modularity_diff = 0, 0

        return -modularity, -modularity_diff

    return local_modularity_score


@cython.annotation_typing(False)
def make_masked_negative_modularity_score_fn(
    graph: NeighborGraph, node_mask: np.ndarray, r: float = 0
):
    neighbors = graph.graph._neighbors
    distances = graph.graph._distances
    affinities = distances_to_affinities_slpi(distances)
    nbhd_boundaries = graph.graph._neighborhood_boundaries
    total_weight = masked_total_weight(
        neighbors, affinities, nbhd_boundaries, node_mask
    )

    def local_modularity_score(node: ClusterNode) -> Tuple[float, float]:
        # TODO: change type
        new_clusters = tuple([c.datapoints for c in node.children])
        if len(new_clusters) > 0:
            modularity, modularity_diff = masked_modularity_change(
                neighbors,
                affinities,
                nbhd_boundaries,
                node_mask,
                new_clusters,
                total_weight,
                r,
            )
        else:
            modularity, modularity_diff = 0, 0

        return -modularity, -modularity_diff

    return local_modularity_score

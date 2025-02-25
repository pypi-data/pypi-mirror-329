# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Interface to Mapper."""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple, Union

import numpy as np
import scipy.sparse as sp

from mapper import nngraph
from mapper.affinities import affinity_functions
from mapper.clustering import compute_partitions_csr_graph
from mapper.config import DEFAULT_KNN_SEED
from mapper.datagraph import (
    DataGraph,
    HierarchicalDataGraph,
    data_graph_from_csr_graph_with_distances,
)
from mapper.matrix import MapperMatrix
from mapper.multiresolution import HierarchicalPartitionGraph
from mapper.neighborgraph import KNNGraph, NeighborGraph, validate_license
from mapper.nerve import partition_set_sizes


def build_knn_graph(
    X: Union[np.ndarray, sp.csr_array],
    metric: str,
    M: int,
    strict_partition: Optional[np.ndarray] = None,
    deduplicate: bool = False,
    seed: int = DEFAULT_KNN_SEED,
) -> Tuple[KNNGraph, np.ndarray]:
    """Build an approximate KNN graph on X.

    Some features will be implemented later.
    """
    # TODO: partitions
    # TODO: deduplication
    # TODO: way to set initial graph
    validate_license()
    node_membership = np.arange(X.shape[0], dtype=np.int32)
    nbrs, distances = nngraph.get_neighbors(X, M, metric, seed=seed)
    knn_graph = KNNGraph(nbrs, distances)
    return knn_graph, node_membership


# TODO: revisit automatic parameter choices
def build_base_graph_auto(
    X: np.ndarray,
    metric: str,
    max_neighbors: int = 50,
    affinity: Literal["slpi", "exponential", "expinv", "gaussian"] = "slpi",
    strict_partition: Optional[np.ndarray] = None,
    deduplicate: Union[bool, Literal["auto"]] = "auto",
    seed: int = DEFAULT_KNN_SEED,
) -> Tuple[DataGraph, dict]:
    """Build a base graph on X, automatically choosing KNN params.

    This follows a backwards-compatible algorithm.
    """
    if deduplicate == "auto":
        deduplicate = metric == "hamming"
    N = X.shape[0]
    M = min(max_neighbors, N)
    knn_graph, node_membership = build_knn_graph(
        X,
        metric,
        M,
        strict_partition=strict_partition,
        deduplicate=deduplicate,
        seed=seed,
    )
    csr_nbr_graph = knn_graph.symmetrized(M, min_nbrs=1)
    n_components_min = csr_nbr_graph.components().max() + 1

    if M < 10:
        params = {"metric": metric, "M": M, "K": M, "min_nbrs": 1, "affinity": affinity}
        return (
            data_graph_from_csr_graph_with_distances(
                csr_nbr_graph.csr_graph, node_membership, affinity
            ),
            params,
        )

    min_nbrs = 1
    for K in range(10, M + 1, 5):
        csr_nbr_graph = knn_graph.symmetrized(K, min_nbrs)
        n_components_k = csr_nbr_graph.components().max() + 1
        if n_components_k == n_components_min:
            break

    upper_bound_min_nbrs = min(10, K) + 1

    for candidate_min_nbrs in range(0, upper_bound_min_nbrs, 2):
        ng_candidate = knn_graph.symmetrized(
            K,
            candidate_min_nbrs,
        )
        components = ng_candidate.components()
        min_component_size = partition_set_sizes(components).min()
        csr_nbr_graph = ng_candidate
        if min_component_size > 10:
            break

    params = {
        "metric": metric,
        "M": M,
        "K": K,
        "min_nbrs": candidate_min_nbrs,
        "affinity": affinity,
    }
    data_graph = data_graph_from_csr_graph_with_distances(
        csr_nbr_graph.csr_graph, node_membership, affinity
    )
    data_graph.raw_graph = knn_graph
    for param, val in params.items():
        setattr(data_graph, param, val)
    data_graph.source_dataset = MapperMatrix(X)
    return data_graph, params


def build_base_datagraph(
    X: np.ndarray,
    metric: str,
    M: int,
    K: int,
    min_nbrs: int,
    affinity: Literal["slpi", "exponential", "expinv", "gaussian"] = "slpi",
    strict_partition: Optional[np.ndarray] = None,
    deduplicate: bool = False,
    seed: int = DEFAULT_KNN_SEED,
    **_,
) -> DataGraph:
    """Build a base graph by creating a KNN graph and symmetrizing.

    Returns a DataGraph that can serve as a drop-in replacement for a
    NeighborGraph.
    """
    knn_graph, node_membership = build_knn_graph(
        X,
        metric,
        M,
        strict_partition=strict_partition,
        deduplicate=deduplicate,
        seed=seed,
    )
    csr_nbr_graph = knn_graph.symmetrized(K, min_nbrs)
    edge_attrs = csr_nbr_graph.csr_graph.edge_attrs
    edge_attrs["weight"] = affinity_functions[affinity](edge_attrs["distance"])
    data_graph = DataGraph(csr_nbr_graph.csr_graph, node_membership=node_membership)
    data_graph.raw_graph = knn_graph
    data_graph.M = M
    data_graph.K = K
    data_graph.min_nbrs = min_nbrs
    data_graph.affinity = affinity
    data_graph.metric = metric
    data_graph.source_dataset = MapperMatrix(X)
    return data_graph


def build_hierarchical_graph_from_base(
    base_graph: DataGraph,
    clustering_params: Dict,
    max_nodes: Optional[int] = None,
    edge_weight_normalize_power: float = 1 / 3,
):
    """Build a HierarchicalDataGraph from a base DataGraph.

    Does not currently support filter functions.

    Params:
        base_graph: A DataGraph whose nodes will be clustered to produce the
            hierarchy of partition graphs.
        clustering_params: A dictionary of parameters for the clustering algorithm.
        max_nodes: The maximum number of nodes a graph may have in order to be
            included in the output. This can avoid creating graphs with large
            numbers of nodes that will not be used.
        edge_weight_normalize_power: Power to raise the normalizing factor to
            when computing weights for edges in the partition graph. This factor is
            the product of the sizes of the nodes joined by the new edge. The
            default of 1/3 is for backwards compatibility with previous
            implementations.
    """
    # TODO: allow specifying additional partitions?
    partitions = compute_partitions_csr_graph(
        base_graph.csr_graph._neighbors,
        base_graph.csr_graph.edge_attrs["weight"],
        base_graph.csr_graph._neighborhood_boundaries,
        clustering_params.get("max_height", 1000),
        clustering_params.get("max_cluster_growth_rate", 2),
        clustering_params.get("min_affinity_ratio", 0.8),
        clustering_params.get("min_n_clusters_ratio", 0.85),
        clustering_params.get("allow_multiple_merges_per_node", False),
    )
    if max_nodes is not None:
        partitions = [p for p in partitions if p.max() < max_nodes]

    levels = [
        base_graph.partition_datagraph(
            partition,
            weight_attr="weight",
            output_weights="normalized",
            weight_normalize_power=edge_weight_normalize_power,
        )
        for partition in partitions
    ]
    return HierarchicalDataGraph(
        levels, base_graph, source_dataset=base_graph.source_dataset
    )


def build_graph(
    X: np.ndarray,
    base_graph_params: Dict,
    filters: List,
    clustering_params: Dict,
) -> HierarchicalDataGraph:
    """Build a hierarchical graph from X."""
    # TODO: filters
    base_graph = build_base_datagraph(X, **base_graph_params)
    hierarchical_graph = build_hierarchical_graph_from_base(
        base_graph, clustering_params
    )
    return hierarchical_graph


def quick_graph_new(
    X: np.ndarray,
    metric: str,
    neighbor_params: Optional[Dict] = None,
    affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
):
    """Create a graph from a dataset and specified metric.

    If neighbor_params is not specified, chooses neighborhood parameters
    automatically. If it is specified, it must be a dictionary containing keys
    "M", "K", and "min_nbrs" with integer values. Increasing any of these values
    will increase the connectivity of the resulting graph."""

    if neighbor_params is None:
        ng, _ = build_base_graph_auto(X, metric, affinity=affinity)
    else:
        ng = build_base_datagraph(X, metric, affinity=affinity, **neighbor_params)
    g = build_hierarchical_graph_from_base(ng, {})
    return g


def quick_graph(
    X: np.ndarray,
    metric: str,
    neighbor_params: Optional[Dict] = None,
    affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
):
    """Create a graph from a dataset and specified metric.

    If neighbor_params is not specified, chooses neighborhood parameters
    automatically. If it is specified, it must be a dictionary containing keys
    "M", "K", and "min_nbrs" with integer values. Increasing any of these values
    will increase the connectivity of the resulting graph."""

    if neighbor_params is None:
        ng = NeighborGraph.with_automatic_params(X, metric)
    else:
        neighbor_params["metric"] = metric
        ng = NeighborGraph(X, **neighbor_params)
    g = HierarchicalPartitionGraph(ng, affinity=affinity)
    return g

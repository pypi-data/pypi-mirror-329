# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Hierarchical partitions of datasets."""

from abc import ABC, abstractmethod
from typing import List, Literal, Optional

import numpy as np

from mapper.affinities import affinity_functions
from mapper.clustering import compute_partitions
from mapper.data_partition import DataPartition
from mapper.matrix import MapperMatrix
from mapper.neighborgraph import (
    GraphPruningPredicate,
    NeighborGraph,
    TrivialPruningPredicate,
)


class HierarchicalDataPartition(ABC):
    """Abstract class representing a nested sequence of partitions of a
    NeighborGraph."""

    n_levels: int
    source_matrix: MapperMatrix

    @abstractmethod
    def get_partition(self, level: int) -> np.ndarray:
        """The binning of data points at a given level of the hierarchy."""


class AverageLinkageClustering(HierarchicalDataPartition):
    """Constructs a hierarchical clustering of a NeighborGraph using the
    algorithm implemented in xshop.

    First converts the edge lengths to affinities (i.e. weights). Then, starting
    with the partition of the graph into individual nodes, merges pairs of
    clusters based on affinity values. The affinity between two clusters is the
    sum of the affinities for all edges between them divided by the product of
    the number of nodes in each cluster.

    At each step, the pair of clusters with the maximum affinity A is found, and
    all pairs of clusters with affinity at least min_affinity * A are merged, as
    long as this does not produce a new cluster of size bigger than
    max_cluster_growth_rate times the previous largest cluster.

    Once this sequence of nested partitions is computed, we drop each partition
    if it does not reduce the number of partitions to at most
    min_n_clusters_ratio times the number of clusters in the previous step.
    """

    # TODO: does the cluster affinity calculation make sense?
    # TODO: allow other methods of calculating the graph affinity

    def __init__(
        self,
        neighbor_graph: NeighborGraph,
        min_affinity: float = 0.8,
        max_cluster_growth_rate: float = 2,
        min_n_clusters_ratio: float = 0.85,
        max_height: int = 500,
        allow_multiple_merges_per_node: bool = False,
        affinity: Literal["slpi", "exponential", "expinv", "gaussian"] = "slpi",
    ):
        self.source_matrix = neighbor_graph.data_matrix
        self.neighbor_graph = neighbor_graph
        self.min_affinity_ratio = min_affinity
        self.max_cluster_growth_rate = max_cluster_growth_rate
        self.min_n_clusters_ratio = min_n_clusters_ratio
        self.max_height = max_height
        self.allow_multiple_merges_per_node = allow_multiple_merges_per_node

        self._partitions: Optional[List[np.ndarray]] = None
        self.n_levels: Optional[int] = None
        self.affinity = affinity
        self.affinity_fn = affinity_functions[affinity]

    def _compute_partitions(self) -> List[np.ndarray]:
        return compute_partitions(
            self.neighbor_graph,
            self.affinity_fn,
            self.max_height,
            self.max_cluster_growth_rate,
            self.min_affinity_ratio,
            self.min_n_clusters_ratio,
            self.allow_multiple_merges_per_node,
        )

    def get_partition(self, level: int) -> np.ndarray:
        """Returns the partition vector at the given level."""
        if self._partitions is None:
            self._partitions = self._compute_partitions()
            self.n_levels = len(self._partitions)

        return self._partitions[level]

    def best_modularity_partition(
        self, max_clusters: Optional[int] = None
    ) -> np.ndarray:
        """Returns the partition vector which gives the best (weighted) modularity
        for the underlying graph. If max_clusters is provided, limit to the
        partition vectors with at most max_clusters distinct sets."""

        top_modularity = -np.inf
        if self._partitions is None:
            self._partitions = self._compute_partitions()
        best_partition = self.get_partition(0)
        for partition in reversed(self._partitions):
            if max_clusters and partition.max() + 1 > max_clusters:
                break
            modularity = self.neighbor_graph.graph.partition_modularity(partition)
            if modularity > top_modularity:
                top_modularity = modularity
                best_partition = partition

        return best_partition

    def __len__(self):
        if self.n_levels is None:
            self._partitions = self._compute_partitions()
            self.n_levels = len(self._partitions)
        return self.n_levels


class FlattenedHierarchicalPartition(DataPartition):
    """Selects one level from a HierarchicalDataPartition to partition a dataset."""

    def __init__(self, hierarchy: HierarchicalDataPartition, level: int):
        self.source_matrix = hierarchy.source_matrix
        self.hierarchy = hierarchy
        self.level = level

    @property
    def domain_partition(self) -> np.ndarray:
        return self.hierarchy.get_partition(self.level)

    @property
    def pruning_predicate(self) -> GraphPruningPredicate:
        return TrivialPruningPredicate()


class LocalFlattenedHierarchicalPartition(DataPartition):
    """Selects one level from a HierarchicalDataPartition to partition a subset
    of a dataset."""

    def __init__(
        self, hierarchy: HierarchicalDataPartition, level: int, domain: np.ndarray
    ):
        self.source_matrix = hierarchy.source_matrix
        self.hierarchy = hierarchy
        self.level = level
        self.domain = domain
        self._domain_partition: Optional[np.ndarray] = None

    @property
    def domain_partition(self) -> np.ndarray:
        if self._domain_partition is None:
            full_partition = self.hierarchy.get_partition(self.level)
            partition = np.full_like(full_partition, full_partition.max() + 1)
            restricted_partition = full_partition[self.domain]
            _, restricted_partition = np.unique(
                restricted_partition, return_inverse=True
            )
            partition[self.domain] = restricted_partition
            self._domain_partition = partition
        return self._domain_partition

    @property
    def pruning_predicate(self) -> GraphPruningPredicate:
        return TrivialPruningPredicate()

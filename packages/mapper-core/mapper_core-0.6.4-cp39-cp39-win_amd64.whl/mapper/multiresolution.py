# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Multiresolution Mapper graphs."""

from abc import ABC, abstractmethod
from typing import Collection, Dict, List, Literal, Optional, Sequence, Tuple

import numpy as np

from mapper.data_partition import DataPartition
from mapper.hierarchical_partition import (
    AverageLinkageClustering,
    FlattenedHierarchicalPartition,
    HierarchicalDataPartition,
)
from mapper.mappergraph import WeightedPartitionGraph
from mapper.neighborgraph import NeighborGraph
from mapper.protocols import NeighborGraphLike, SourceDataLike


class AbstractGraph(ABC):
    """A graph whose nodes represent subsets of a source dataset."""

    source_dataset: Optional[SourceDataLike]

    @property
    @abstractmethod
    def nodes(self) -> Sequence[Collection]:
        """A list with one entry for each node, where entry i contains the data
        point ids represented in node i."""

    @property
    @abstractmethod
    def edge_list(self) -> List[Tuple[int, int]]:
        """List of tuples ``(i,j)`` representing edges i->j.

        Edges should be interpreted as undirected, and only the direction with
        ``i < j`` will be included in the list.
        """

    @property
    @abstractmethod
    def edge_mtx(self) -> np.ndarray:
        """A list of edges in numpy array form.

        Array is of shape ``(n_edges, 2)``, and ``edge_mtx[k, :] = [i, j]`` for an edge
        i->j.
        """

    @property
    @abstractmethod
    def edge_weights(self) -> np.ndarray:
        """Nonnegative weights for each edge."""

    @property
    @abstractmethod
    def n_edges(self) -> int:
        """Number of edges in the graph."""

    @property
    @abstractmethod
    def edges(self) -> List[Dict]:
        """A list of dictionaries representing data for each edge.

        The dictionary for an edge will contain at least "source", "target", and
        "weight" keys, but may contain additional data.
        """

    def to_dict(self) -> Dict:
        """Representation of the graph as a dictionary.

        Has keys "nodes" and "edges", where the entry for "nodes" is
        ``self.nodes``, and the entry for "edges" is ``self.edges``.
        """

        return {
            "nodes": self.nodes,
            "edges": self.edges,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(source_dataset={self.source_dataset}, "
            f"n_nodes={len(self.nodes)}, n_edges={self.n_edges})"
        )


class MultiResolutionGraph(ABC):
    """A graph with multiple resolution scales.

    There are n_levels different graphs arranged in a hierarchical way. Each
    node of the graph at level i represents a subset of data points, and is a
    subset of some node of the graph at each level j > i.
    """

    n_levels: int
    source_dataset: Optional[SourceDataLike]

    neighbor_graph: NeighborGraphLike

    @property
    @abstractmethod
    def levels(self) -> List[AbstractGraph]:
        """A list of graphs representing the dataset at multiple resolution scales."""

    # @abstractmethod
    # def node_map(self, source_level, target_level) -> Dict:
    #     pass

    def to_dicts(self):
        """Produces a dictionary representation of every graph in self.levels."""
        return [g.to_dict() for g in self.levels]

    def __len__(self):
        return self.n_levels

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(source_dataset={self.source_dataset}, "
            f"n_levels={self.n_levels})"
        )


class DisjointPartitionGraph(AbstractGraph):
    """A graph whose nodes represent disjoint subsets of a dataset."""

    def __init__(
        self,
        neighbor_graph: NeighborGraph,
        filters: List[DataPartition],
        L_coarseness: int,
        L_connectivity: int,
        distance_threshold: float = np.inf,
        affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
    ):
        self.neighbor_graph = neighbor_graph
        self.filters = filters
        self.L_coarseness = L_coarseness
        self.L_connectivity = L_connectivity
        self.distance_threshold = distance_threshold
        self.full_partition_graph = WeightedPartitionGraph(
            self.neighbor_graph,
            self.filters,
            self.L_coarseness,
            self.L_connectivity,
            distance_threshold=self.distance_threshold,
            min_edge_weight=0,
            affinity=affinity,
        )
        self.source_dataset = self.neighbor_graph.data_matrix

    @property
    def nodes(self) -> Sequence[Collection]:
        return self.full_partition_graph.cover.sets

    @property
    def node_membership(self) -> np.ndarray:
        """An array with one entry for each data point indicating the node to
        which that data point belongs."""

        return self.full_partition_graph.partition.membership_vec

    @property
    def edge_list(self) -> List[Tuple[int, int]]:
        return self.full_partition_graph.edge_list

    @property
    def edge_mtx(self) -> np.ndarray:
        return self.full_partition_graph.weighted_edge_list[0]

    @property
    def edge_weights(self) -> np.ndarray:
        return self.full_partition_graph.weighted_edge_list[1]

    @property
    def n_edges(self) -> int:
        return len(self.edge_weights)

    @property
    def edges(self) -> List[Dict]:
        return [
            {"source": i, "target": j, "weight": w}
            for ((i, j), w) in zip(self.edge_list, self.edge_weights)
        ]


class HierarchicalPartitionGraph(MultiResolutionGraph):
    """A MultiResolutionGraph built with a hierarchical partition."""

    def __init__(
        self,
        neighbor_graph: NeighborGraph,
        hierarchical_partition: Optional[HierarchicalDataPartition] = None,
        filters: Optional[List[DataPartition]] = None,
        L_coarseness: Optional[int] = None,
        L_connectivity: Optional[int] = None,
        distance_threshold: float = np.inf,
        affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
    ):
        self.neighbor_graph = neighbor_graph
        self.filters = filters if filters else []
        self.hierarchical_partition = (
            hierarchical_partition
            if hierarchical_partition is not None
            else AverageLinkageClustering(self.neighbor_graph, affinity=affinity)
        )
        self.L_coarseness = (
            L_coarseness if L_coarseness is not None else self.neighbor_graph.M
        )
        self.L_connectivity = (
            L_connectivity if L_connectivity is not None else self.neighbor_graph.M
        )
        self.distance_threshold = distance_threshold
        self.affinity = affinity

        self._levels = None
        self.source_dataset = self.neighbor_graph.data_matrix

    @property
    def levels(self) -> List[DisjointPartitionGraph]:
        if self._levels is None:
            self._levels = [
                DisjointPartitionGraph(
                    self.neighbor_graph,
                    [FlattenedHierarchicalPartition(self.hierarchical_partition, level)]
                    + self.filters,
                    self.L_coarseness,
                    self.L_connectivity,
                    self.distance_threshold,
                    affinity=self.affinity,
                )
                for level in range(len(self.hierarchical_partition))
            ]
        return self._levels

    @property
    def n_levels(self):
        return len(self.levels)

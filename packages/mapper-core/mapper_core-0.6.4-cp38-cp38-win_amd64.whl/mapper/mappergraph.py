# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""The MapperGraph abstract class, implemented by PartitionGraph."""

from __future__ import annotations

from abc import abstractmethod
from typing import Dict, List, Literal, Optional, Tuple, Union

import cython
import networkx as nx
import numpy as np
from cython.cimports.libc.stdint import int32_t, int64_t
from cython.cimports.libcpp.pair import pair
from cython.cimports.libcpp.vector import vector

from mapper.cover import Cover, Partition
from mapper.data_partition import DataPartition
from mapper.neighborgraph import CSRNeighborGraph, NeighborGraph

numeric = cython.fused_type(cython.float, cython.double, int32_t, int64_t)


class MapperGraph:
    """Manages the computation of a final Mapper graph from a neighbor graph.

    Abstract, currently only implemented as a PartitionGraph (or
    WeightedPartitionGraph). Should maintain references to the NeighborGraph and
    Filters used to generate the output, and computes the output graph only when
    requested, caching the result.
    """

    def __init__(
        self,
        neighbor_graph: NeighborGraph,
        filters: List[DataPartition],
        L_coarseness: int,
        L_connectivity: int,
    ):
        """Params:

        neighbor_graph: the underlying NeighborGraph structure. Used to
        determine the edges of the output graph.

        filters: a list of Filter objects that define the partition on the
        underlying dataset.

        L_coarseness: the maximum edge rank to keep when splitting the
        filter partition into connected components

        L_connectivity: the maximum edge rank to keep when expanding the partition
        into a cover.
        """
        super().__init__()
        self.neighbor_graph = neighbor_graph

        if len(filters) == 0:
            raise ValueError("At least one filter function must be specified.")

        # for filt in filters:
        #     if neighbor_graph.data_matrix is not filt.parent_dataset:
        #         # TODO: when parent_dataset is implemented, raise a warning here
        #         pass

        self.filters = filters
        self.L_coarseness = L_coarseness
        self.L_connectivity = L_connectivity
        self._cover = None

    @property
    @abstractmethod
    def cover(self) -> Cover:
        pass

    @property
    @abstractmethod
    def edge_list(self) -> List[Tuple[int, int]]:
        pass

    def with_new_params(self, L_coarseness: int, L_connectivity: int) -> MapperGraph:
        """Returns a (possibly) new MapperGraph object with new parameters.

        Reuses itself when parameters did not change.
        """
        # TODO: is there any way to save more computation?
        if L_coarseness == self.L_coarseness and L_connectivity == self.L_connectivity:
            return self
        else:
            return self.__class__(
                self.neighbor_graph, self.filters, L_coarseness, L_connectivity
            )

    def as_networkx(self) -> nx.Graph:
        """Returns the graph as a networkx.Graph object."""
        g = nx.Graph()
        g.add_nodes_from(range(len(self.cover.sets)))
        g.add_edges_from(self.edge_list)
        return g

    def data_dict(self, vertex_key: str = "nodes", edge_key: str = "edges") -> Dict:
        """Returns a dictionary containing the graph connectivity and associated
        node indices in a visjs-friendly format."""

        edge_list = [{"id": f"{s}->{t}", "from": s, "to": t} for s, t in self.edge_list]
        vertex_list = [
            {"id": i, "idxs": [int(x) for x in u]}
            for i, u in enumerate(self.cover.sets)
        ]
        return {vertex_key: vertex_list, edge_key: edge_list}

    def param_dict(self) -> Dict:
        """Returns a dictionary containing a human-readable description of the
        parameters used to create this graph."""

        param_dict = {
            "filters": {i: str(f) for i, f in enumerate(self.filters)},
            "L_coarseness": self.L_coarseness,
            "L_connectivity": self.L_connectivity,
            "M": self.neighbor_graph.M,
            "K": self.neighbor_graph.K,
            "metric": str(self.neighbor_graph.metric),
        }
        return param_dict


class PartitionGraph(MapperGraph):
    """Manages the computation of the final Mapper graph from a neighbor graph
    and filters.

    Computes the coarsened graph by partitioning the nodes of the neighbor graph
    using the Filters, making each set of the partition a node, and placing
    edges between nodes when there exists at least one edge between them in the
    original graph.
    """

    def __init__(
        self,
        neighbor_graph: NeighborGraph,
        filters: List[DataPartition],
        L_coarseness: int,
        L_connectivity: int,
        distance_threshold: float = np.inf,
    ):
        super().__init__(neighbor_graph, filters, L_coarseness, L_connectivity)

        self.distance_threshold = distance_threshold

        self._pruned_graph: Optional[CSRNeighborGraph] = None
        self._cover: Optional[Cover] = None
        self._partition: Optional[Partition] = None
        self._edge_list: Optional[List[Tuple[int, int]]] = None

    def _compute_partition(self):
        filter_partitions = [fil.domain_partition for fil in self.filters]
        partition = self.neighbor_graph.connected_components_of_partitions(
            filter_partitions,
            self.L_coarseness,
            self.distance_threshold,
        )
        return partition

    def _compute_pruned_graph(self):
        return self.neighbor_graph.graph.pruned_by_predicates(
            [fil.pruning_predicate for fil in self.filters], self.L_connectivity
        )

    @property
    def cover(self) -> Cover:
        if self._cover is None:
            self._cover = self.partition.as_cover()
        return self._cover

    @property
    def partition(self) -> Partition:
        if self._partition is None:
            self._partition = self._compute_partition()
        return self._partition

    @property
    def pruned_graph(self) -> CSRNeighborGraph:
        if self._pruned_graph is None:
            self._pruned_graph = self._compute_pruned_graph()
        return self._pruned_graph

    @property
    def edge_list(self) -> List[Tuple[int, int]]:
        if self._edge_list is None:
            self._edge_list = self.pruned_graph.partition_graph_edge_list(
                self.partition, self.cover
            )
        return list(self._edge_list)

    def with_new_params(
        self,
        L_coarseness: Optional[int] = None,
        L_connectivity: Optional[int] = None,
        distance_threshold: Optional[float] = None,
    ) -> PartitionGraph:
        L_coarseness = L_coarseness if L_coarseness is not None else self.L_coarseness
        L_connectivity = (
            L_connectivity if L_connectivity is not None else self.L_connectivity
        )
        distance_threshold = (
            distance_threshold
            if distance_threshold is not None
            else self.distance_threshold
        )
        new_pg = PartitionGraph(
            self.neighbor_graph,
            self.filters,
            L_coarseness,
            L_connectivity,
            distance_threshold,
        )
        if (
            L_coarseness == self.L_coarseness
            and distance_threshold == self.distance_threshold
        ):
            # pylint: disable=protected-access
            new_pg._partition = self._partition
            new_pg._cover = self._cover
            if L_connectivity == self.L_connectivity:
                new_pg._pruned_graph = self._pruned_graph
                new_pg._edge_list = self._edge_list
        return new_pg

    def __repr__(self) -> str:
        neighbor_graph = str(self.neighbor_graph)
        filters = "\n".join([str(f) for f in self.filters])
        lines = [
            (
                f"PartitionGraph(L_coarseness={self.L_coarseness}, "
                f"L_connectivity={self.L_connectivity})"
            ),
            f"NeighborGraph:\n{neighbor_graph}",
            f"Filters:\n{filters}",
        ]
        r = "\n".join(lines)
        return r


class WeightedPartitionGraph(PartitionGraph):
    """PartitionGraph with edges filtered by an affinity-based weight rather
    than minimum rank.

    This class is experimental. Its functionality and interface may change
    without warning in the future.

    The weights of the edges in the partition graph are computed by summing the
    weights of the underlying edges in the NeighborGraph, and scaling by a
    factor that varies with the number of data points in each partition. This
    way of ranking edges is finer-grained and typically more representative of
    the actual strength of connections between data points, particularly when
    nodes contain large numbers of points.
    """

    def __init__(
        self,
        neighbor_graph: NeighborGraph,
        filters: List[DataPartition],
        L_coarseness: int,
        L_connectivity: int,
        min_edge_weight: Optional[Union[float, int]] = None,
        n_edges: Optional[int] = None,
        distance_threshold: float = np.inf,
        affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
    ):
        super().__init__(
            neighbor_graph, filters, L_coarseness, L_connectivity, distance_threshold
        )
        self.affinity = affinity
        if n_edges is not None:
            self.n_edges = n_edges
            self.min_edge_weight = None
        elif min_edge_weight is not None:
            self.min_edge_weight = min_edge_weight
            self.n_edges = None
        else:
            raise ValueError("One of min_edge_weight and n_edges must be set")
        self._weighted_edge_list: Optional[Tuple[np.ndarray, np.ndarray]] = None

    @property
    def edge_list(self) -> List[Tuple[int, int]]:
        if self._edge_list is None:
            edges, weights = self.weighted_edge_list
            if self.n_edges is not None:
                self._edge_list = edge_list_from_weighted_list_n_edges(
                    edges, self.n_edges
                )
            else:
                self._edge_list = edge_list_from_weighted_list_threshold(
                    edges, weights, self.min_edge_weight
                )

        return list(self._edge_list)

    @property
    def weighted_edge_list(self) -> Tuple[np.ndarray, np.ndarray]:
        if self._weighted_edge_list is None:
            edges, weights = self.pruned_graph.weighted_partition_graph_edge_list(
                self.partition, self.cover, affinity=self.affinity
            )
            sizes = np.array([len(u) for u in self.cover.sets])
            rescaled_sizes = sizes ** (2 / 3)
            weight_scaling_factor = (
                rescaled_sizes[edges[:, 0]] * rescaled_sizes[edges[:, 1]]
            )
            weights *= weight_scaling_factor
            weight_ordering = np.flip(np.argsort(weights))
            sorted_edges = edges[weight_ordering, :]
            sorted_weights = weights[weight_ordering]
            self._weighted_edge_list = (sorted_edges, sorted_weights)
        return self._weighted_edge_list

    def with_new_params(
        self,
        L_coarseness: Optional[int] = None,
        L_connectivity: Optional[int] = None,
        distance_threshold: Optional[float] = None,
        min_edge_weight: Optional[float] = None,
        n_edges: Optional[int] = None,
    ) -> WeightedPartitionGraph:
        L_coarseness = L_coarseness if L_coarseness is not None else self.L_coarseness
        L_connectivity = (
            L_connectivity if L_connectivity is not None else self.L_connectivity
        )
        min_edge_weight = (
            min_edge_weight if min_edge_weight is not None else self.min_edge_weight
        )
        distance_threshold = (
            distance_threshold
            if distance_threshold is not None
            else self.distance_threshold
        )
        new_pg = WeightedPartitionGraph(
            self.neighbor_graph,
            self.filters,
            L_coarseness,
            L_connectivity,
            min_edge_weight,
            n_edges,
            distance_threshold,
        )
        if (
            L_coarseness == self.L_coarseness
            and distance_threshold == self.distance_threshold
        ):
            # pylint: disable=protected-access
            new_pg._partition = self._partition
            new_pg._cover = self._cover
            if L_connectivity == self.L_connectivity:
                new_pg._pruned_graph = self._pruned_graph
                new_pg._weighted_edge_list = self._weighted_edge_list
                if (
                    min_edge_weight == self.min_edge_weight
                    and self.min_edge_weight is not None
                ):
                    new_pg._edge_list = self._edge_list
        return new_pg


@cython.boundscheck(False)
@cython.wraparound(False)
def edge_list_from_weighted_list_n_edges(edges: int32_t[:, ::1], n_edges: int32_t):
    N: cython.Py_ssize_t = min(n_edges, edges.shape[0])
    edge_list: vector[pair[int32_t, int32_t]] = vector[pair[int32_t, int32_t]]()
    i: cython.Py_ssize_t
    u: int32_t
    v: int32_t
    e: pair[int32_t, int32_t]
    for i in range(N):
        # bounds: i < N < edges.shape[0]
        u = edges[i, 0]
        v = edges[i, 1]
        e = pair[int32_t, int32_t](u, v)
        edge_list.push_back(e)

    return list(edge_list)


@cython.boundscheck(False)
@cython.wraparound(False)
def edge_list_from_weighted_list_threshold(
    edges: int32_t[:, ::1], weights: cython.float[::1], threshold: numeric
):
    N: cython.Py_ssize_t = edges.shape[0]
    edge_list: vector[pair[int32_t, int32_t]] = vector[pair[int32_t, int32_t]]()
    i: cython.Py_ssize_t
    u: int32_t
    v: int32_t
    e: pair[int32_t, int32_t]
    for i in range(N):
        # bounds: i < N < edges.shape[0] = len(weights)
        if weights[i] < threshold:
            break
        # bounds: i < N < edges.shape[0]
        u = edges[i, 0]
        v = edges[i, 1]
        e = pair[int32_t, int32_t](u, v)
        edge_list.push_back(e)
    return edge_list

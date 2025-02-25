# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.


# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

import cython
import numpy as np

from mapper.multiresolution import DisjointPartitionGraph, HierarchicalPartitionGraph


@cython.cclass
@dataclass
class ClusterNode:
    """A node in a hierarchical tree of clusters."""

    datapoints: np.ndarray[Any, np.dtype[np.int32]]
    min_level: cython.int
    children: List[ClusterNode]
    parent: Optional[ClusterNode] = None
    modularity_increase: Optional[float] = None
    local_score: Optional[float] = None
    local_score_change: Optional[float] = None

    def __eq__(self, other):
        return self is other


class ClusterTree:
    """A hierarchical tree of clusters."""

    def __init__(self, levels: List[List[ClusterNode]], start_level: int = 0):
        self.start_level = start_level
        self.end_level = len(levels) - 1
        self._levels = levels

    @classmethod
    def from_graph_with_constraints(
        cls,
        graph: HierarchicalPartitionGraph,
        max_n_clusters: int,
        min_cluster_size: int = 1,
    ) -> ClusterTree:
        start_level = find_graph_level(graph, max_n_clusters, min_cluster_size)
        levels = _make_cluster_tree_local(graph, start_level)
        return cls(levels, start_level)

    @classmethod
    def from_subgraph_with_constraints(
        cls,
        graph: HierarchicalPartitionGraph,
        subset: np.ndarray,
        max_n_clusters: int,
        min_cluster_size: int = 1,
    ) -> ClusterTree:
        start_level = find_graph_level(graph, max_n_clusters, min_cluster_size)
        levels = _make_cluster_tree_local(graph, start_level, subset)
        return cls(levels, start_level)

    @property
    def top_level(self) -> List[ClusterNode]:
        return self._levels[-1]


def find_graph_level(
    graph: HierarchicalPartitionGraph,
    max_n_clusters: int,
    min_cluster_size: int = 1,
) -> int:
    """Find the lowest level in a multiresolution graph satisfying constraints.

    The level selected will have at most `max_n_clusters`, and all clusters in
    that level will have size at least `min_cluster_size`.
    """
    start_level = len(graph.levels) - 1
    for i, g in reversed(list(enumerate(graph.levels))):
        if len(g.nodes) > max_n_clusters:
            start_level = min(i + 1, len(graph.levels) - 1)
            break
        if any(len(n) < min_cluster_size for n in g.nodes):
            start_level = min(i + 1, len(graph.levels) - 1)
            break
    else:
        start_level = 0
    return start_level


def _get_level_clusters(
    g: DisjointPartitionGraph, level: int, subset: Optional[np.ndarray] = None
) -> Tuple[List[ClusterNode], Optional[np.ndarray]]:
    """Instantiates a list of ClusterNode objects for each node in g.

    If subset is provided, will restrict to nodes that intersect with subset,
    and restrict the clusters to subset.
    """
    if subset is not None:
        node_indices = np.unique(g.node_membership[subset]).astype(np.int32)
        clusters = [
            ClusterNode(
                datapoints=np.intersect1d(subset, g.nodes[i]).astype(np.int32),
                min_level=level,
                children=[],
            )
            for i in node_indices
        ]
    else:
        node_indices = None
        clusters = [
            ClusterNode(
                datapoints=np.asarray(u, dtype=np.int32),
                min_level=level,
                children=[],
            )
            for u in g.nodes
        ]
    return clusters, node_indices


# TODO: this should probably be part of the MultiResolutionGraph interface
def _make_cluster_tree_local(
    graph: HierarchicalPartitionGraph,
    start_level: int,
    subset: Optional[np.ndarray] = None,
) -> List[List[ClusterNode]]:
    """Finds the hierarchy of node sets in a MultiResolutionGraph.

    Returns a list of lists of ClusterNodes, with one list for each layer in the
    MultiResolutionGraph. Each ClusterNode is linked to its parent node and its
    children nodes. ClusterNode objects are reused in multiple layers if a
    cluster stays the same.

    All nodes can be accessed from the top layer; the only extra information
    provided by the rest of the list is what the original coarseness clustering
    levels were.

    If subset is provided, restricts to nodes of the graph that contain at least
    one data point in the subset, and restricts the clusters to the data points
    in that subset.
    """
    use_subset = subset is not None
    if use_subset:
        subset_mask = np.zeros(
            graph.levels[-1].node_membership.shape[0], dtype=np.bool_
        )
        subset_mask[subset] = 1

    g = graph.levels[start_level]

    first_level_clusters, _ = _get_level_clusters(g, start_level, subset)

    cluster_tree = [first_level_clusters]

    for level, g in zip(
        range(start_level + 1, len(graph.levels)),
        graph.levels[start_level + 1 :],
    ):
        # using the node_membership attribute requires that our graph be a
        # HierarchicalPartitionGraph, not just any MultiResolutionGraph
        cluster_membership = g.node_membership
        clusters, node_indices = _get_level_clusters(g, level, subset)

        # at each iteration, link the newly created nodes to the nodes in the last level
        for c_child in cluster_tree[-1]:
            parent_node_id = cluster_membership[c_child.datapoints[0]]
            if node_indices is not None:
                # need to reindex into the subset of clusters we're working with
                parent_ix = np.searchsorted(node_indices, parent_node_id)
            else:
                parent_ix = parent_node_id
            c_parent = clusters[parent_ix]

            if len(c_parent.datapoints) > len(c_child.datapoints):
                # attach the parent to the child
                c_child.parent = c_parent
                c_parent.children.append(c_child)
            elif len(c_parent.datapoints) == len(c_child.datapoints):
                # the parent is the same as the child so we can use the same object
                # and discard the new parent object we created
                clusters[parent_ix] = c_child

        cluster_tree.append(clusters)

        if len(clusters) == 1:
            # we've found a node that contains all the points we're clustering
            break

    return cluster_tree

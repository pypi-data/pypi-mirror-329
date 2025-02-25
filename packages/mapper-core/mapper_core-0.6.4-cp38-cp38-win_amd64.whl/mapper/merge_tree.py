# cython: infer_types=True, language_level=3
# distutils: language = c++
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set

import cython
import numpy as np
from cython.cimports.libc.math import INFINITY
from cython.cimports.libc.stdint import int32_t

from mapper.graph import CSRGraph

# A merge tree (sometimes also called a split tree, and related to contour
# trees) is associated with a graph G and a function f on the nodes of G.  This
# tree consists of a number of *segments*, each of which is associated with one
# or more nodes of G. Each segment also has a *birth level* and a *death level*,
# as well as 0 or more *parents* and 0 or 1 *children*. (This terminology may be
# a bit backwards from what you expect for trees, in that parent segments join
# together to produce a single child. The motivation for this is that if we use
# this terminology, a parent is born before its children.)

# A fundamental property of a merge tree is that if you choose a threshold value
# t and select all segments alive at time t, these correspond with the connected
# components of the subgraph of G consisting of nodes for which f(v) > t.
# The idea is that the branches of the merge tree track how connected components
# of the superlevel sets of f merge together as we reduce the threshold.

# The structure of the merge tree is perhaps simplest to explain by describing the
# algorithm for constructing one. We start with an empty tree, and iterate
# through the nodes of G in decreasing value of f. For each node v, we look at all
# of its neighboring nodes and their associated segments, if any. Three things
# can happen:
# 1. The node is not adjacent to any active segments
# 2. The node is adjacent to nodes in exactly one active segment s
# 3. The node is adjacent to nodes in more than one active segment, a set we will call N
# In case 1, we create a new segment, with birth value f(v), and mark it as active.
# In case 2, we add v to the segment s and continue.
# In case 3, we merge the segments v is adjacent to by doing the following:
# - mark each segment s' in N as inactive, and give it death value f(v)
# - create a new segment s, containing v and all nodes in the segments in N.
# - mark s as the child of each segment in N
# - add N as the set of parents of s.

# data structure: collection of branches. each branch has a birth and death
# time, the nodes contained in the branch immediately before death, and a
# reference to a successor branch.

# what do we do with the nodes that cause death? one option is to just add them
# to the successor branch but not represent them anywhere else.

# the algorithm should work by adding nodes in order of function values.  when a
# node is added, we can create a new branch with only that node and the
# appropriate birth time, add the node to a branch, or kill two or more branches
# and create a new branch which is a successor branch. this can result in
# branches of length 0, which we then need to clean up.


@cython.cclass
@dataclass
class MergeSegment:
    birth_level: cython.double
    death_level: cython.double
    lifetime: cython.double
    nodes: list[cython.int]
    successor_idx: Optional[int] = None
    parent_idxs: Optional[list[int]] = None
    stability: float = -np.inf
    cumulative_stability: float = -np.inf
    selected: bool = False


@cython.cclass
@dataclass
class MergeTree:
    segments: List[MergeSegment]
    f: np.ndarray

    # The idea of stability comes from the HDBSCAN* algorithm
    # https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html
    # The stability of a segment in the merge tree that is born at $b$ and dies
    # at $d$ is equal to \sum_v min(f(v), b) - d

    # The idea is that we want clusters that contain a lot of nodes that stick
    # around for a long time. The largest value stability can take is N * (b - d),
    # where N is the number of nodes in the branch.  It can take values arbitrarily
    # close to b - d, if all but one node join just before the death level.
    # The interpretation of the score obviously depends on the range/distribution of f.

    # "good" clusters look like a group of nodes that all join fairly early and stay
    # together for a while before the cluster merges with another one. If a cluster
    # only sticks around for a little while, we probably either want to use its
    # parents or its child.

    # We also add the option for a multiplicative weight on each node, for a
    # couple of reasons.
    # One is that each node can represent a different number of data points, and it
    # probably makes sense to measure stability by number of data points included
    # and not just the number of nodes.
    # The other is that we also want to emphasize clusters with high values of the
    # failure function, not just clusters that persist across a wide range of values
    # of the failure function. So we can use a weight to tip the scales toward
    # clusters with high failure values.

    # Choosing branches to return is done by selecting a disjoint set of branches
    # whose total stability is as large as possible. This can be done by starting at
    # the initial branches and moving downwards in the tree, selecting a child
    # branch only if that branch's stability is greater than the sum of its
    # parents'.

    def compute_stability_and_select_branches(
        self,
        node_weights: np.ndarray,
        min_birth_level: float = 0,
    ):
        """Select semgents of a merge tree based on a stability score.

        For a segment that is born at level b and dies at level d, the stability is
        equal to ∑_v (min(b, f(v)) - d) * w(v). The algorithm selects a disjoint
        collection of segments which has the greatest possible total stability
        subject to the constraint that every segment is born before min_birth_level.
        """
        # deselect everything in case this has been run previously
        for segment in self.segments:
            segment.selected = False

        for segment in self.segments:
            if len(segment.nodes) == 0:
                continue
            f_vals = self.f[segment.nodes]
            stability = np.sum(
                (np.minimum(segment.birth_level, f_vals) - segment.death_level)
                * node_weights[segment.nodes]
            )
            segment.stability = stability
            if not segment.parent_idxs:
                segment.selected = True
        for segment in self.segments:
            # It is ok to just loop through in this order (rather than do a tree
            # traversal) because the segments are in a topologically sorted order
            # for the tree, so we will never process a segment before its parents.
            segment.cumulative_stability = segment.stability
            if not segment.parent_idxs:
                continue
            parent_stability = sum(
                [self.segments[i].cumulative_stability for i in segment.parent_idxs]
            )
            if parent_stability > segment.stability:
                segment.cumulative_stability = parent_stability
                segment.selected = False
            elif segment.birth_level > min_birth_level:
                segment.selected = True
                deselect_parents(segment, self.segments)

    @staticmethod
    def from_csr_graph(g: CSRGraph, f: np.ndarray) -> MergeTree:
        # TODO: support mask?
        return graph_merge_tree_internal_cython(
            g._neighbors, g._neighborhood_boundaries, f
        )


# TODO: use C++ stdlib data structures for better performance?
@cython.boundscheck(False)
@cython.wraparound(False)
def graph_merge_tree_internal_cython(
    neighbors: int32_t[::1], neighborhood_boundaries: int32_t[::1], f: np.ndarray
) -> MergeTree:
    segments: List[MergeSegment] = []
    # INVARIANT: values in node_to_branch are always valid indices into segments
    node_to_branch: Dict[int, int] = {}
    ordered_nodes: cython.Py_ssize_t[:] = np.argsort(f)[::-1]
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    jdx: cython.Py_ssize_t

    for i in ordered_nodes:
        neighbor_branches: Set[int] = set()
        # bounds: i + 1 < len(f) + 1 = n_nodes + 1 = len(neighborhood_boundaries)
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            # bounds: jdx < max(neighborhood_boundaries) = len(neighbors)
            j = neighbors[jdx]
            if j in node_to_branch:
                # bounds: checked explicitly
                neighbor_branches.add(node_to_branch[j])

        if len(neighbor_branches) == 1:
            # add this node to the appropriate branch
            branch_idx = next(iter(neighbor_branches))
            # bounds: branch_idx is in neighbor_branches, contains valid branch ids
            segments[branch_idx].nodes.append(i)
            # INVARIANT: branch_idx comes from neighbor_branches
            # this consists of values pulled from node_to_branch
            # so invariant is preserved
            node_to_branch[i] = branch_idx
        elif len(neighbor_branches) > 1:
            # this node will merge these branches together
            new_branch_id = len(segments)
            new_segment = MergeSegment(
                # bounds: 0 <= i < len(f)
                birth_level=f[i],
                death_level=-INFINITY,
                lifetime=INFINITY,
                nodes=[i],
                successor_idx=None,
                parent_idxs=list(neighbor_branches),
            )
            for branch_idx in neighbor_branches:
                # bounds: branch_idx is from neighbor_branches, which comes from
                # node_to_branch, which always has valid indices into segments
                segments[branch_idx].death_level = f[i]
                segments[branch_idx].successor_idx = new_branch_id
                new_segment.nodes.extend(segments[branch_idx].nodes)
            segments.append(new_segment)
            for node in new_segment.nodes:
                # INVARIANT: new_branch_id is one past the end of segments
                # until new_segment is appended, when it is the last valid index.
                # so when it is added to node_to_branch, this is a valid index
                node_to_branch[node] = new_branch_id
        else:
            # create a new singleton branch
            new_branch_id = len(segments)
            new_segment = MergeSegment(
                # bounds: 0 <= i < len(f)
                birth_level=f[i],
                death_level=-INFINITY,
                lifetime=INFINITY,
                nodes=[i],
                successor_idx=None,
                parent_idxs=[],
            )
            segments.append(new_segment)
            # INVARIANT: new_branch_id is one past the end of segments
            # until new_segment is appended, when it is the last valid index.
            # so when it is added to node_to_branch, this is a valid index
            node_to_branch[i] = new_branch_id

    # set all remaining branch deaths to the lowest value of f
    # bounds: len(ordered_nodes) = len(f)
    min_f = f[ordered_nodes[f.shape[0] - 1]]
    for segment in segments:
        if segment.death_level == -np.inf:
            segment.death_level = min_f
        segment.lifetime = segment.birth_level - segment.death_level

    filter_zero_lifetime_segments(segments)
    filter_death_level_nodes(segments, f)

    return MergeTree(segments=segments, f=f)


def filter_zero_lifetime_segments(segments: List[MergeSegment]):
    """Remove segments of lifetime zero from a merge tree.

    These can be spuriously produced by the merge tree algorithm when multiple
    nodes have the same function value and should be combined into their
    successors.

    This function does not remove the corresponding objects from the list, so
    that index references are still valid. However, all nodes are removed from
    the orphaned segments, so they can be identified after the fact.
    """
    for i, segment in enumerate(segments):
        if segment.lifetime == 0 and segment.successor_idx is not None:
            successor = segments[segment.successor_idx]
            assert successor.birth_level == segment.death_level
            successor.parent_idxs.remove(i)
            if segment.parent_idxs is not None:
                successor.parent_idxs.extend(segment.parent_idxs)
            segment.nodes = []
            segment.successor_idx = None
            segment.parent_idxs = None


# TODO: figure out why this is as slow as it is
def filter_death_level_nodes(segments: List[MergeSegment], f: np.ndarray):
    """Ensure that all nodes in a segment are born strictly before the death level.

    Segments breaking this invariant can be created when multiple nodes have the
    same function value. In this case, we move any nodes born at the death level
    to the successor segment.
    """
    for segment in segments:
        death_nodes_mask = f[segment.nodes] == segment.death_level
        n_death_nodes = np.sum(death_nodes_mask)
        if n_death_nodes == 0:
            continue
        # if it's a final segment, it's ok to equal the death level
        if segment.successor_idx is not None:
            # the nodes are already included in the successor, so we just need
            # to delete them from this segment
            segment.nodes = np.array(segment.nodes)[~death_nodes_mask].tolist()


def deselect_parents(segment: MergeSegment, segments: List[MergeSegment]):
    if segment.parent_idxs:
        for i in segment.parent_idxs:
            segments[i].selected = False
            deselect_parents(segments[i], segments)

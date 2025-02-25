# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.


# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++

from typing import Callable, List, Tuple, Union

import numpy as np

from mapper.cluster_tree import ClusterNode, ClusterTree

# General framework for choosing a clustering: we greedily try to optimize some
# scoring function of the global partition by starting with the trivial
# partition and subdividing nodes.  This requires calculating the change in the
# score function due to splitting one or more nodes, which we can think of as a
# sort of gradient. If the score function is cheap, we can just do the
# differencing approach. Also if the score function decomposes as a sum over
# clusters you just need to look at the cluster you're changing.  And we already
# have a method to get the change in modularity. We can try to impose
# constraints as well, but there's no guarantee of finding a feasible solution
# even if one exists. Another way to treat constraints is by some kind of
# lexicographic order, where solutions with constraints satisfied dominate those
# without constraints satisfied, but then within constraints, better scores
# dominate. This at least means you always get a solution.

# we could also start somewhere in the middle (top scoring level of the graph?)
# and look at moves both up and down. I don't think this is a lot more
# complicated than the splitting-only case.

LocalClusterScoreFunction = Callable[[ClusterNode], Tuple[float, float]]
GlobalClusterScoreFunction = Callable[[List[ClusterNode]], float]


def trivial_global_score_fn(_) -> float:
    return 0


def _clear_cached_tree_data(node: ClusterNode):
    node.local_score = None
    node.local_score_change = None
    node.modularity_increase = None
    for n in node.children:
        _clear_cached_tree_data(n)


def _get_local_score_diff_cached(
    node: ClusterNode, score_fns: List[LocalClusterScoreFunction]
) -> float:
    if node.local_score_change is None:
        node.local_score = 0
        node.local_score_change = 0
        for score_fn in score_fns:
            score, score_change = score_fn(node)
            node.local_score += score
            node.local_score_change += score_change
    return node.local_score_change


def split_cluster(clusters: List[ClusterNode], split_idx: int):
    return [
        *clusters[:split_idx],
        *clusters[split_idx].children,
        *clusters[split_idx + 1 :],
    ]


def split_clusters_to_max_size(
    current_clustering: List[ClusterNode],
    max_cluster_size: Union[int, float],
) -> List[ClusterNode]:
    """Splits clusters until every cluster has at most max_cluster_size points."""
    cluster_was_split = True
    while cluster_was_split:
        cluster_was_split = False
        for i, c in enumerate(current_clustering):
            cluster_size = len(c.datapoints)
            cluster_has_children = len(c.children) > 0
            if cluster_size > max_cluster_size and cluster_has_children:
                current_clustering = split_cluster(current_clustering, i)
                cluster_was_split = True

    return current_clustering


def _get_node_split_score_diff(
    current_clustering: List[ClusterNode],
    node_ix: int,
    local_score_fns: List[LocalClusterScoreFunction],
    global_score_fn: GlobalClusterScoreFunction,
    global_score: float,
    min_cluster_size: int,
    max_n_clusters: float,
) -> float:
    """Returns the change in the clustering score from splitting this node.

    If the split is not admissible, returns infinity.
    """
    c = current_clustering[node_ix]

    split_n_clusters = len(current_clustering) + len(c.children) - 1
    split_children_are_large_enough = all(
        len(u.datapoints) >= min_cluster_size for u in c.children
    )
    split_has_children = len(c.children) > 0
    split_is_admissible = (
        split_children_are_large_enough
        and split_n_clusters < max_n_clusters
        and split_has_children
    )

    if split_is_admissible:
        candidate_clustering = split_cluster(current_clustering, node_ix)
        # computes the aggregated local score if it's not already cached
        return (
            _get_local_score_diff_cached(c, local_score_fns)
            + global_score_fn(candidate_clustering)
            - global_score
        )

    else:
        # TODO: maybe a better way of signaling a cluster should not be split
        return np.inf


def choose_best_split(
    current_clustering: List[ClusterNode],
    local_score_fns: List[LocalClusterScoreFunction],
    global_score_fn: GlobalClusterScoreFunction,
    min_cluster_size: int,
    max_n_clusters: float,
) -> Tuple[int, float]:
    """Choose the best cluster to split based on given score functions.

    This relies on state stored in the ClusterNode objects, so it should be used
    with caution.
    """
    global_score = global_score_fn(current_clustering)

    # contains the change in score that would result from splitting each
    # cluster in the current clustering
    score_diff = np.array(
        [
            _get_node_split_score_diff(
                current_clustering,
                i,
                local_score_fns,
                global_score_fn,
                global_score,
                min_cluster_size,
                max_n_clusters,
            )
            for i in range(len(current_clustering))
        ]
    )

    best_split_ix = np.argmin(score_diff)
    split_improvement = -score_diff[best_split_ix]

    return best_split_ix, split_improvement


def optimize_cluster_score_top_down(
    cluster_tree: ClusterTree,
    local_score_fns: List[LocalClusterScoreFunction],
    global_score_fn: GlobalClusterScoreFunction = trivial_global_score_fn,
    min_cluster_size: int = 1,
    max_cluster_size: Union[int, float] = np.inf,
    max_n_clusters: float = np.inf,
    min_n_clusters: int = 1,
    min_improvement: float = 0,
) -> List[np.ndarray]:
    """Tries to find a partition minimizing a scoring function.

    This scoring function is computed as the sum of a global scoring function,
    which scores an entire clustering holistically, and a number of local scoring
    functions, which each decompose as the sum of a function applied to each
    cluster in a clustering.

    Minimization works by beginning at the top level of the cluster tree, and
    iteratively splitting the cluster that will give the largest decrease in the
    score function. A split is not considered if it will produce a cluster
    smaller than `min_cluster_size` or will lead to more than `max_n_clusters`
    clusters. The process terminates when no admissible split would yield a
    greater decrease in the score than specified by `min_improvement`, unless
    there are still fewer than `min_n_clusters` clusters, in which case the
    "least bad" split is taken.

    Args:
        cluster_tree: The hierarchical cluster tree in which to search for an
            optimal clustering.
        local_score_fns: A list of local scoring functions that will be added together.
        global_score_fn: A global scoring function.
        min_cluster_size: Size of the smallest cluster allowed in the returned
            clustering. If a cluster split would produce a smaller cluster, it is
            inadmissible.
        max_cluster_size: Size of the largest cluster allowed in the returned
            clustering. Clusters larger than this will be split unconditionally
            (unless they have no children).
        max_n_clusters: Maximum number of clusters to return. If a cluster split
            would produce more clusters, it is inadmissible.
        min_n_clusters: Minimum number of clusters to return. If no admissible
            split yields a sufficient improvement in the score, the "least bad"
            split will be taken. If there are no admissible splits, the optimization
            will terminate.
        min_improvement: The minimum amount the score function needs to decrease
            in order to split a cluster. Larger values make it harder to find a
            "good enough" split. Note that this can be set to a negative value, in
            which case a split that increases the score function may be performed,
            as long as the increase is not too large. This may be useful in
            combination with the other constraints.
    """
    # TODO: start somewhere other than the top?
    # TODO: allow cluster merges as well
    # TODO: nicer way of handling constraints?

    if min_n_clusters > max_n_clusters:
        err_msg = (
            f"min_n_clusters={min_n_clusters} cannot be "
            f"greater than max_n_clusters={max_n_clusters}."
        )
        raise ValueError(err_msg)

    if min_cluster_size > max_cluster_size:
        err_msg = (
            f"min_cluster_size={min_cluster_size} cannot be "
            f"greater than max_cluster_size={max_cluster_size}."
        )
        raise ValueError(err_msg)

    current_clustering = cluster_tree.top_level
    for c in current_clustering:
        _clear_cached_tree_data(c)

    # first, split until all clusters are smaller than max_cluster_size,
    # ignoring score function
    current_clustering = split_clusters_to_max_size(
        current_clustering, max_cluster_size
    )

    # now iteratively make the best split until constraints are met and there
    # are no more score improvements to be had
    while True:
        best_split_ix, split_improvement = choose_best_split(
            current_clustering,
            local_score_fns,
            global_score_fn,
            min_cluster_size,
            max_n_clusters,
        )

        not_enough_clusters = len(current_clustering) < min_n_clusters

        should_split_cluster = (split_improvement > min_improvement) or (
            not_enough_clusters and split_improvement > -np.inf
        )

        if should_split_cluster:
            current_clustering = split_cluster(current_clustering, best_split_ix)
        else:
            # if we can't split the best cluster, there's nothing left to do
            break

    return [c.datapoints for c in current_clustering]

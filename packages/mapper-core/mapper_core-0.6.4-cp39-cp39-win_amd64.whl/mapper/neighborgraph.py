# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""The NeighborGraph class, which is the basic data structure managing the
nearest neighbors in a dataset."""

from __future__ import annotations

import base64
import json
import os
import sys
import traceback
from abc import abstractmethod
from datetime import datetime
from hashlib import md5
from typing import Any, Callable, List, Literal, Optional, Tuple, Union

import msgpack  # type: ignore
import networkx as nx
import numpy as np
import pytz
import requests
from dateutil import parser
from dotenv import load_dotenv

from mapper._csr_graph import (
    prune_filter_mask_csr,
    prune_filter_mask_csr_frac,
    prune_filter_mask_csr_local,
    prune_filters_mask_csr,
)
from mapper.affinities import affinity_functions
from mapper.config import DEFAULT_KNN_SEED
from mapper.cover import Cover, Partition
from mapper.exceptions import SerializationError
from mapper.graph import CSRGraph
from mapper.matrix import MapperMatrix
from mapper.nerve import (
    partition_graph_edge_list_csr,
    partition_set_sizes,
    weighted_partition_graph_edge_list_csr,
)
from mapper.nngraph import (
    get_knn_edge_list,
    get_neighbors,
    normalize_distances,
    rerank_nbhds,
    symmetrize_distances,
    symmetrize_neighbors,
    to_symmetric_csr,
)
from mapper.serialization import np_from_bytes, np_to_bytes


# this is a class rather than just a standalone function so we can serialize it
# more easily.
class GraphPruningPredicate:
    @abstractmethod
    def prune_graph(self, graph: CSRNeighborGraph) -> np.ndarray:
        """Returns a mask for the edges of a CSRNeighborGraph."""


class TrivialPruningPredicate(GraphPruningPredicate):
    """Performs no pruning."""

    def prune_graph(self, graph: CSRNeighborGraph) -> np.ndarray:
        return graph.mask


class FunctionValuePruningPredicate(GraphPruningPredicate):
    """Prunes the edges of a graph based on values of a function on its nodes.

    prune_vals should be a 1-d array with the same number of data points as the
    graph, and pruning_threshold is a nonnegative number. An edge between two
    nodes whose function values differ by more than pruning_threshold will be
    masked off.
    """

    def __init__(self, prune_vals: np.ndarray, pruning_threshold: Union[int, float]):
        self.prune_vals = prune_vals
        self.pruning_threshold = pruning_threshold

    def prune_graph(self, graph: CSRNeighborGraph) -> np.ndarray:
        # pylint: disable=protected-access
        mask = prune_filter_mask_csr(
            graph._neighbors,
            graph._neighborhood_boundaries,
            self.prune_vals,
            self.pruning_threshold,
        )
        return mask


class PercentOverlapPruningPredicate(GraphPruningPredicate):
    def __init__(
        self,
        filter_vals: np.ndarray,
        range_partition: np.ndarray,
        domain_partition: np.ndarray,
        pruning_threshold: float,
    ):
        self.filter_vals = filter_vals
        self.range_partition = range_partition
        self.domain_partition = domain_partition
        self.pruning_threshold = pruning_threshold
        interval_widths = np.diff(self.range_partition)
        self.upper_bounds = np.zeros_like(interval_widths)
        self.upper_bounds[:-1] = range_partition[1:-1] + (
            pruning_threshold * interval_widths[1:]
        )
        self.upper_bounds[-1] = np.inf
        self.lower_bounds = np.zeros_like(interval_widths)
        self.lower_bounds[1:] = range_partition[1:-1] - (
            pruning_threshold * interval_widths[:-1]
        )
        self.lower_bounds[0] = -np.inf

    def prune_graph(self, graph: CSRNeighborGraph) -> np.ndarray:
        mask = prune_filter_mask_csr_frac(
            graph._neighbors,
            graph._neighborhood_boundaries,
            self.filter_vals,
            self.domain_partition,
            self.lower_bounds,
            self.upper_bounds,
        )
        return mask


class LocalFunctionValuePruningPredicate(GraphPruningPredicate):
    """Prunes edges based on a function value only within a subset of nodes."""

    def __init__(
        self,
        prune_vals: np.ndarray,
        pruning_threshold: Union[int, float],
        domain: np.ndarray,
    ):
        self.prune_vals = prune_vals
        self.pruning_threshold = pruning_threshold
        self.domain = domain

    def prune_graph(self, graph: CSRNeighborGraph) -> np.ndarray:
        # pylint: disable=protected-access
        mask = prune_filter_mask_csr_local(
            graph._neighbors,
            graph._neighborhood_boundaries,
            self.prune_vals,
            self.pruning_threshold,
            self.domain,
        )
        return mask


class KNNGraph:
    """A directed graph storing the M nearest neighbors of each point in a dataset.

    Stores the list of neighbors and the distance to each neighbor. The storage
    format is optimized for storing precisely M neighbors. Can be converted into
    an undirected graph by symmetrizing, which produces a CSRNeighborGraph.
    """

    _serialization_version = 2

    def __init__(
        self,
        neighbors: np.ndarray,
        distances: np.ndarray,
    ):
        super().__init__()
        self._neighbors = neighbors
        self._distances = distances
        self.N = neighbors.shape[0]
        self.M = neighbors.shape[1]
        self._edge_list = None

    @property
    def edge_list(self) -> List[Tuple[np.int32, np.int32]]:
        if self._edge_list is None:
            self._edge_list = get_knn_edge_list(
                self._neighbors,
            )
        return self._edge_list

    def symmetrized(self, K: int, min_nbrs: int = 1) -> CSRNeighborGraph:
        """Returns a symmetrized version of this graph.

        Roughly speaking, keeps up to K edges v -> u incident to a vertex v, if
        and only if v is also at least an Mth nearest neighbor of u. Will always
        keep edges of rank <= min_nbrs.
        """
        if K > self.M:
            raise ValueError(f"K={K} must be <= M={self.M}")
        neighbors, distances, n_neighbors = symmetrize_neighbors(
            self._neighbors, self._distances, K, min_nbrs
        )
        distances = normalize_distances(neighbors, distances, n_neighbors)
        distances = symmetrize_distances(neighbors, distances, n_neighbors)
        neighbors, distances, n_neighbors = rerank_nbhds(
            neighbors, distances, n_neighbors
        )
        (
            csr_neighbors,
            csr_distances,
            csr_nbhd_boundaries,
            csr_edge_ranks,
        ) = to_symmetric_csr(neighbors, distances, n_neighbors)
        return CSRNeighborGraph.from_raw_data(
            csr_neighbors, csr_distances, csr_nbhd_boundaries, csr_edge_ranks
        )

    def as_networkx(self) -> nx.DiGraph:
        """Returns this graph as a networkx.DiGraph instance."""
        # every node has (outgoing) neighbors, so all nodes will show up here
        return nx.DiGraph(self.edge_list)

    def truncated(self, M: int) -> KNNGraph:
        """Returns a version of this graph with the maximum number of neighbors
        truncated to M."""

        if M > self.M:
            raise ValueError(
                (
                    f"New value for M ({M}) "
                    f"must be less than current value for M ({self.M})."
                )
            )
        neighbors = np.ascontiguousarray(self._neighbors[:, :M])
        distances = np.ascontiguousarray(self._distances[:, :M])
        g = KNNGraph(neighbors, distances)
        return g

    def to_msgpack(self) -> bytes:
        """Save all data to a msgpack object."""

        neighbors_bytes = np_to_bytes(self._neighbors)
        distances_bytes = np_to_bytes(self._distances)
        data = {
            "obj_type": "KNNGraph",
            "version": self._serialization_version,
            "neighbors": neighbors_bytes,
            "distances": distances_bytes,
        }
        return msgpack.packb(data)  # type: ignore

    @classmethod
    def from_msgpack(cls, data: bytes) -> KNNGraph:
        """Instantiate a new RawNeighborGraph from a serialized version.

        Raises SerializationError if the serialized object is the wrong type or
        from a different version of the code.
        """

        data_dict: dict = msgpack.unpackb(data)
        if data_dict["obj_type"] != "KNNGraph":
            raise SerializationError(
                f"Incorrect serialized object type {data_dict['obj_type']}."
            )
        if data_dict["version"] != cls._serialization_version:
            raise SerializationError(
                f"Incorrect serialization version {data_dict['version']}. "
                f"Expected {cls._serialization_version}."
            )
        neighbors = np_from_bytes(data_dict["neighbors"])
        distances = np_from_bytes(data_dict["distances"])

        return KNNGraph(neighbors, distances)


class CSRNeighborGraph:
    """An undirected neighbor graph stored in a symmetric CSR adjacency format.

    Each edge has an associated (float) distance and (integer) rank. In
    addition, a boolean mask can be added to ignore any number of edges. This
    mask is expected to be symmetric.

    N is the number of nodes, M is the maximum node degree, L is the maximum
    edge rank used.
    """

    _serialization_version = 4

    def __init__(
        self,
        csr_graph: CSRGraph,
    ):
        self.csr_graph = csr_graph
        self._edge_list: Optional[List[Tuple[int, int]]] = None

    @classmethod
    def from_raw_data(
        cls,
        neighbors: np.ndarray,
        distances: np.ndarray,
        neighborhood_boundaries: np.ndarray,
        edge_ranks: np.ndarray,
        mask: Optional[np.ndarray] = None,
    ):
        csr_graph = CSRGraph(
            neighbors,
            neighborhood_boundaries,
            edge_attrs={"distance": distances, "rank": edge_ranks},
            mask=mask,
        )
        return CSRNeighborGraph(csr_graph)

    @property
    def N(self) -> int:
        return self.csr_graph.n_nodes

    @property
    def M(self) -> int:
        return self.csr_graph.max_degree

    @property
    def _neighbors(self) -> np.ndarray:
        return self.csr_graph._neighbors

    @property
    def _neighborhood_boundaries(self) -> np.ndarray:
        return self.csr_graph._neighborhood_boundaries

    @property
    def mask(self) -> np.ndarray:
        return self.csr_graph.mask

    @property
    def _distances(self) -> np.ndarray:
        return self.csr_graph.edge_attrs["distance"]

    @property
    def _edge_ranks(self) -> np.ndarray:
        return self.csr_graph.edge_attrs["rank"]

    @property
    def edge_list(self) -> List[Tuple[np.int32, np.int32]]:
        if self._edge_list is None:
            self._edge_list = self.csr_graph.get_edge_list()
        return self._edge_list

    def components(self) -> np.ndarray:
        """Connected components of this graph, as a vector with a component id
        for each node."""
        return self.csr_graph.get_components()

    def pruned_by_predicates(
        self, preds: List[GraphPruningPredicate], L: int
    ) -> CSRNeighborGraph:
        """A copy of this graph with edges pruned as defined by a DataPartition."""

        # make a copy to avoid modifying the mask
        mask = self.mask.copy()
        for pred in preds:
            mask = mask & pred.prune_graph(self)

        mask = mask & (self._edge_ranks < L)

        return CSRNeighborGraph(self.csr_graph.with_mask(mask))

    def pruned(
        self, prune_vecs: List[np.ndarray], thresholds: Union[List, np.ndarray], L: int
    ) -> CSRNeighborGraph:
        """A copy of this graph with edges pruned using function values.

        For each array f in prune_vecs, removes any edge u ~ v where the
        difference |f[u]-[v]| is greater than the corresponding value in
        thresholds. Also removes any edges of rank greater than L.
        """
        mask = prune_filters_mask_csr(
            self._neighbors, self._neighborhood_boundaries, prune_vecs, thresholds
        )
        mask = mask & (self._edge_ranks < L)
        return CSRNeighborGraph(self.csr_graph.with_mask(self.mask & mask))

    def refine_partitions(
        self, partitions: List[np.ndarray], L: int, distance_threshold: float
    ) -> np.ndarray:
        """Connected components of each set in the joint partition refinement.

        Given a collection of partition vectors of the neighborhood graph,
        computes the connected components of each set in their joint refinement.
        The edges of the graph are restricted to those of rank < min(L, self.L).
        """

        mask = prune_filters_mask_csr(
            self._neighbors,
            self._neighborhood_boundaries,
            partitions,
            np.zeros(len(partitions)),
        )
        mask = mask & (self._distances <= distance_threshold)
        mask = mask & (self._edge_ranks < L)
        return self.csr_graph.with_mask(mask).refine_partitions(partitions)

    def partition_graph_edge_list(
        self,
        partition: Partition,
        cover: Cover,
        weighted: bool = False,
        affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
    ) -> List[Tuple[int, int]]:
        if weighted:
            affinity_fn = affinity_functions[affinity]
            weights = affinity_fn(self._distances)
            return weighted_partition_graph_edge_list_csr(
                self._neighbors,
                weights,
                self._neighborhood_boundaries,
                self._edge_ranks,
                self.mask,
                self.M,
                partition.membership_vec,
                cover.sets,
            )
        return partition_graph_edge_list_csr(
            self._neighbors,
            self._neighborhood_boundaries,
            self._edge_ranks,
            self.mask,
            self.M,
            partition.membership_vec,
            cover.sets,
        )

    def weighted_partition_graph_edge_list(
        self,
        partition: Partition,
        cover: Cover,
        affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
    ) -> Tuple[np.ndarray, np.ndarray]:
        affinity_fn = affinity_functions[affinity]
        weights = affinity_fn(self._distances)
        return weighted_partition_graph_edge_list_csr(
            self._neighbors,
            weights,
            self._neighborhood_boundaries,
            self._edge_ranks,
            self.mask,
            self.M,
            partition.membership_vec,
            cover.sets,
        )

    def partition_modularity(
        self,
        partition_vec: np.ndarray,
        affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
    ):
        """Compute the modularity score for the given partition on this graph.

        This is the difference between the (weighted) fraction of edges inside
        each set of the partition and the expected fraction of edges in that set if
        the graph were randomly rewired while preserving node degrees.
        """
        affinity_fn = affinity_functions[affinity]
        weights = affinity_fn(self._distances)
        self.csr_graph.edge_attrs["weight"] = weights
        return self.csr_graph.partition_modularity(partition_vec, "weight")

    def as_networkx(self) -> nx.Graph:
        """Returns this graph as a networkx.Graph instance."""
        return self.csr_graph.as_networkx()

    def to_msgpack(self) -> bytes:
        """Save all data to a msgpack object."""
        graph_data = self.csr_graph.to_msgpack()
        data = {
            "obj_type": "CSRNeighborGraph",
            "version": self._serialization_version,
            "csr_graph": graph_data,
        }
        return msgpack.packb(data)  # type: ignore

    @classmethod
    def from_msgpack(cls, data: bytes) -> CSRNeighborGraph:
        """Instantiate a new RawNeighborGraph from a serialized version.

        Raises SerializationError if the serialized object is the wrong type or
        from a different version of the code.
        """

        data_dict: dict = msgpack.unpackb(data)
        if data_dict["obj_type"] != "CSRNeighborGraph":
            raise SerializationError(
                f"Incorrect serialized object type {data_dict['obj_type']}."
            )
        if data_dict["version"] != cls._serialization_version:
            raise SerializationError(
                f"Incorrect serialization version {data_dict['version']}. "
                f"Expected {cls._serialization_version}."
            )
        csr_graph = CSRGraph.from_msgpack(data_dict["csr_graph"])

        return CSRNeighborGraph(csr_graph)


class NeighborGraph:
    """The symmetrized neighborhood graph of a dataset.

    Stores a reference to the original dataset, and lazily computes the graph
    when needed. Can return a version of itself with new parameters, reusing
    previously computed pieces when possible.
    """

    # TODO: implement metrics available in xshop, including variation of
    # information and random forest distances

    # TODO: implement metrics in a more uniform, serializable way
    _serialization_version = 5

    def __init__(
        self,
        data_matrix: Union[MapperMatrix, Any],
        M: int,
        K: int,
        metric: Union[str, Callable] = "euclidean",
        min_nbrs: int = 1,
        affinity_fn: Literal["slpi", "exponential", "gaussian"] = "slpi",
        seed: int = DEFAULT_KNN_SEED,
        seed_graph: Optional[KNNGraph] = None,
    ):
        """Params:

        data_matrix: a MapperMatrix or numpy array containing source data.
        If a numpy array, it will be converted into a MapperMatrix.

        M: total number of neighbors to compute

        K: symmetrization threshold for neighbors. Essentially, a link will
        be kept if it is in the top K neighbors in at least one direction.

        min_nbrs: a minimum number of neighbors to keep for each point,
        regardless of M and K

        metric: a string or numba-compiled function giving the distance metric

        seed: random seed to initialize the approximate nearest neighbors
        search. Should be a positive integer less than 2**32.
        """
        validate_license()

        self.data_matrix = (
            data_matrix
            if isinstance(data_matrix, MapperMatrix)
            else MapperMatrix(data_matrix)
        )
        self.N = self.data_matrix.shape[0]
        if self.N <= M:
            raise ValueError(f"M={M} must be < N={self.N}.")
        self.M = M
        if K > self.M:
            raise ValueError(f"K={K} must be <= M={self.M}.")
        self.K = K
        self.min_nbrs = min_nbrs
        self.metric = metric
        self.affinity_fn = affinity_fn
        self.seed = seed
        self.seed_graph = seed_graph
        self._raw_graph: Optional[KNNGraph] = None
        self._sym_graph: Optional[CSRNeighborGraph] = None

    @staticmethod
    def with_automatic_params(
        data_matrix: Union[np.ndarray, MapperMatrix],
        metric: str = "euclidean",
        seed: int = DEFAULT_KNN_SEED,
    ) -> NeighborGraph:
        """Constructs a NeighborGraph with automatically chosen K, M, and min_nbrs."""

        N = data_matrix.shape[0]
        M = min(50, N - 1)
        K = min(10, N - 1)
        min_nbrs = 1
        ng_large = NeighborGraph(
            data_matrix, M=M, K=M, metric=metric, min_nbrs=min_nbrs, seed=seed
        )
        n_components_min = ng_large.graph.components().max() + 1

        if K < 10:
            return ng_large

        ng_k = ng_large
        k = K
        for k in range(K, M, 5):
            ng_k = ng_large.with_new_params(M, k, metric, min_nbrs)
            n_components_k = ng_k.graph.components().max() + 1
            if n_components_k == n_components_min:
                break

        upper_bound_min_nbrs = min(10, K) + 1

        optimal_ng = ng_k
        for candidate_min_nbrs in range(0, upper_bound_min_nbrs, 2):
            ng_candidate = ng_k.with_new_params(
                M, k, metric, min_nbrs=candidate_min_nbrs
            )
            components = ng_candidate.graph.components()
            min_component_size = partition_set_sizes(components).min()
            optimal_ng = ng_candidate
            if min_component_size > 10:
                break

        return optimal_ng

    @property
    def raw_graph(self) -> KNNGraph:
        if self._raw_graph is None:
            if self.seed_graph is None:
                neighbors, distances = get_neighbors(
                    self.data_matrix.X, self.M, self.metric, seed=self.seed
                )
            # pylint: disable=protected-access
            else:
                neighbors, distances = get_neighbors(
                    self.data_matrix.X,
                    self.M,
                    self.metric,
                    init_graph=self.seed_graph._neighbors,
                    init_dist=self.seed_graph._distances,
                    seed=self.seed,
                )
            self._raw_graph = KNNGraph(neighbors, distances)
        return self._raw_graph

    @property
    def graph(self) -> CSRNeighborGraph:
        if self._sym_graph is None:
            self._sym_graph = self.raw_graph.symmetrized(self.K, self.min_nbrs)
        return self._sym_graph

    def connected_components_of_partitions(
        self, partitions: List[np.ndarray], L: int, distance_threshold: float = np.inf
    ) -> Partition:
        partition_vec = self.graph.refine_partitions(partitions, L, distance_threshold)
        return Partition(self.data_matrix, partition_vec)

    def with_new_params(
        self, M: int, K: int, metric: str, min_nbrs: int, seed: Optional[int] = None
    ) -> NeighborGraph:
        """Returns a copy of this NeighborGraph with new parameters.

        Reuses already-computed pieces when possible.
        """
        if seed is None:
            seed = self.seed
        ng = NeighborGraph(self.data_matrix, M, K, metric, min_nbrs, seed)
        if metric == self.metric and self._raw_graph is not None:
            # pylint: disable=protected-access
            if M == self.M:
                ng._raw_graph = self._raw_graph
                if K == self.K and min_nbrs == self.min_nbrs:
                    ng._sym_graph = self._sym_graph
            elif M < self.M:
                ng._raw_graph = self._raw_graph.truncated(M)
            else:
                ng.seed_graph = self._raw_graph
        return ng

    def __repr__(self) -> str:
        return "\n".join(
            [
                (f"NeighborGraph(M={self.M}, K={self.K}, " f"metric={self.metric}"),
                f"Dataset: {self.data_matrix}",
            ]
        )

    def hash_id(self) -> str:
        """A unique id derived from the parameters of this object.

        The exact method is subject to change in future versions.
        """

        param_string = (
            str(self.data_matrix.to_msgpack())
            + str(self.M)
            + str(self.K)
            + str(self.metric)
            + str(self.min_nbrs)
            + str(self.seed)
            + str(self.seed_graph)
        )
        return md5(param_string.encode("utf-8")).hexdigest()

    def to_msgpack(self) -> bytes:
        """Save all data to a msgpack object."""

        data = {
            "obj_type": "NeighborGraph",
            "version": self._serialization_version,
            "data_matrix": self.data_matrix.to_msgpack(),
            "M": self.M,
            "K": self.K,
            "metric": self.metric,
            "min_nbrs": self.min_nbrs,
            "seed": self.seed,
        }
        if self._raw_graph is not None:
            data["raw_graph"] = self._raw_graph.to_msgpack()
        if self._sym_graph is not None:
            data["sym_graph"] = self._sym_graph.to_msgpack()
        if self.seed_graph is not None:
            data["seed_graph"] = self.seed_graph.to_msgpack()

        return msgpack.packb(data)  # type: ignore

    def load_from_msgpack(self, data: bytes):
        """Loads the computed RawNeighborGraphs from a serialized NeighborGraph.

        If the parameters of the serialized graph do not match this graph's
        parameters, raises a SerializationError. Otherwise, loads any computed graphs
        into the object and returns self.
        """

        data_dict: dict = msgpack.unpackb(data)
        if data_dict["obj_type"] != "NeighborGraph":
            raise SerializationError(
                f"Incorrect serialized data type {data_dict['obj_type']}."
            )
        if data_dict["version"] != self._serialization_version:
            raise SerializationError(
                f"Incorrect serialization version {data_dict['version']}. "
                f"Expected {self._serialization_version}."
            )
        if data_dict["data_matrix"] != self.data_matrix.to_msgpack():
            raise SerializationError(
                "Serialized source dataset does not match this object's source dataset."
            )
        if (
            data_dict["M"] != self.M
            or data_dict["K"] != self.K
            or data_dict["metric"] != self.metric
            or data_dict["min_nbrs"] != self.min_nbrs
            or data_dict["seed"] != self.seed
        ):
            raise SerializationError(
                "Serialized parameters do not match this object's parameters."
            )
        if "raw_graph" in data_dict:
            self._raw_graph = KNNGraph.from_msgpack(data_dict["raw_graph"])
            if "sym_graph" in data_dict:
                self._sym_graph = CSRNeighborGraph.from_msgpack(data_dict["sym_graph"])
        elif "seed_graph" in data_dict:
            self.seed_graph = KNNGraph.from_msgpack(data_dict["seed_graph"])

        return self


CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "cobalt", "cobalt.json")
OFFLINE_LICENSE_PATH = os.path.join(
    os.path.expanduser("~"), ".config", "cobalt", "license.lic"
)

# can be used to disable license checking globally
LICENSE_KEY_REQUIRED = True

# key to use if no license is found, can be deactivated remotely
DEFAULT_KEY = "9796F1-472793-3AC7DD-9F1498-EBDE95-V3"


def get_license_key():
    license_key_from_env = os.environ.get("COBALT_LICENSE_KEY")
    if not license_key_from_env:
        try:
            with open(CONFIG_PATH) as config_file:
                config_data = json.load(config_file)
            license_key = config_data.get("license_key")
            if not license_key:
                return DEFAULT_KEY
        except Exception:
            return DEFAULT_KEY
    else:
        license_key = license_key_from_env
    return license_key


def check_license():
    if not LICENSE_KEY_REQUIRED:
        return {"valid": True, "message": None}
    check_offline_license_result = check_offline_license()
    if (
        not check_offline_license_result["valid"]
        and not check_offline_license_result["message"]
    ):
        # no license file found, check online now
        check_license_result = call_license_api()
    else:
        # license file is in place
        check_license_result = check_offline_license_result
    return check_license_result


def validate_license():
    check_license_result = check_license()
    if not check_license_result["valid"]:
        raise_exception(check_license_result["message"])


def check_license_expiration_soon():
    check_license_result = check_license()
    if check_license_result["valid"] and check_license_result["message"]:
        # set expiration popup
        return check_license_result["message"]


def check_license_manually():
    check_license_result = check_license()

    if check_license_result["valid"] and not check_license_result["message"]:
        print("License is VALID.")
    elif check_license_result["valid"] and check_license_result["message"]:
        print(
            f"License is valid but will expire soon. {check_license_result['message']} "
            "Contact support@bluelightai.com to extend your license."
        )
    else:
        print(f"License is NOT VALID. {check_license_result['message']}")


def call_license_api():
    load_dotenv()
    check_license_result = {"valid": False, "message": None}
    license_key = get_license_key()
    account_id = os.environ.get(
        "KEYGEN_ACCOUNT_ID", "21957da7-b2d4-4c0b-9119-51006c94bff4"
    )

    if not license_key or not account_id:
        formatted_error_message = (
            "License key not found. Please ensure the COBALT_LICENSE_KEY "
            "environment variable is set to your license key. "
            "See https://docs.cobalt.bluelightai.com/setup.html#license-key-authentication "  # noqa: E501
            "for more details and contact support@bluelightai.com with any questions."
        )
        check_license_result["message"] = formatted_error_message
        return check_license_result

    resp = get_license_data_by_key(license_key)
    if 500 <= resp.status_code < 600:
        check_license_result["message"] = (
            "Could not connect to license server. "
            "Please check that your firewall allows HTTPS connections to "
            "api.keygen.sh. Contact support@bluelightai.com with any questions."
        )
        return check_license_result

    response = resp.json()

    if "errors" in response:
        formatted_message = format_errors(response)

    elif response["meta"]["valid"]:
        check_license_result["valid"] = True

        formatted_message = calculate_expiration_soon(response)
        check_license_result["message"] = formatted_message
        return check_license_result

    elif not response["meta"]["valid"] and response["meta"]["code"] == "NOT_FOUND":
        formatted_message = (
            "Invalid license key. Check that the COBALT_LICENSE_KEY environment "
            "variable is set to your license key. "
            "See https://docs.cobalt.bluelightai.com/setup.html#license-key-authentication "  # noqa: E501
            "for more details and contact support@bluelightai.com with any questions."
        )

    elif not response["meta"]["valid"] and response["meta"]["code"] == "EXPIRED":
        formatted_message = (
            "License is expired. "
            "Contact support@bluelightai.com to extend your license."
        )
    else:
        formatted_message = (
            "Unknown license error occurred. Please contact support@bluelightai.com."
        )

    check_license_result["message"] = formatted_message

    return check_license_result


def format_errors(response):
    errs = response["errors"]

    def format_error(e):
        return "{} - {}".format(e["title"], e["detail"]).lower()

    formatted_errors = map(format_error, errs)
    formatted_message = (
        "License error occurred. Please contact support@bluelightai.com "
        "with the following information: {}"
    ).format(",".join(formatted_errors))
    return formatted_message


WARN_EXPIRATION_DAYS = 3


def calculate_expiration_soon(response):
    message = None
    date_now_str = response["meta"]["ts"]
    date_expiration_str = response["data"]["attributes"]["expiry"]
    if not date_expiration_str:
        # dev license without expiration
        return message

    # Parse the date strings to datetime objects
    date_now = parser.parse(date_now_str)
    date_expiration = parser.parse(date_expiration_str)

    # Calculate the difference in days between the two dates
    delta = date_expiration - date_now
    default_message = "Your Cobalt license will expire soon. "
    if delta.days < 0:
        raise ValueError("License is expired")
    if delta.days <= WARN_EXPIRATION_DAYS:
        message = default_message + f"{delta.days} days left until license expiration"
    if delta.days <= 1:
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        message = (
            default_message
            + f"{hours} hours, {minutes} minutes until license expiration."
        )
    if message:
        message = message + " Please contact support@bluelightai.com to renew."
    return message


def check_offline_license():
    check_license_result = {"valid": False, "message": None}
    license_key = get_license_key()
    if not license_key:
        formatted_error_message = (
            "License key not found. Please ensure the COBALT_LICENSE_KEY "
            "environment variable is set to your license key. "
            "See https://docs.cobalt.bluelightai.com/setup.html#license-key-authentication "  # noqa: E501
            "for more details and contact support@bluelightai.com with any questions."
        )
        check_license_result["message"] = formatted_error_message
        return check_license_result

    if license_key == DEFAULT_KEY:
        # default key must be checked against the server
        return check_license_result

    try:
        decrypted_data = get_data_from_offline_license(license_key)
    except OSError:
        return check_license_result
    except ValueError as e:
        check_license_result["message"] = str(e)
    except Exception as e:
        check_license_result["message"] = f"Unknown error: {str(e)}"
    else:
        date_now = datetime.now(pytz.utc)
        # Format time in keygen format
        formatted_utc_time = date_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        date_now_str = str(formatted_utc_time)
        expiration_time = decrypted_data["data"]["attributes"]["expiry"]
        response = {
            "data": {"attributes": {"expiry": expiration_time}},
            "meta": {"ts": date_now_str},
        }
        try:
            check_license_result["message"] = calculate_expiration_soon(response)
        except ValueError as e:
            check_license_result["message"] = str(e)
        else:
            check_license_result["valid"] = True

    return check_license_result


def get_data_from_offline_license(license_key):
    license_file = read_license_file(path=OFFLINE_LICENSE_PATH)
    data = parse_license_payload(license_file=license_file)

    enc = data["enc"]
    sig = data["sig"]
    alg = data["alg"]

    verify_algorithm(alg=alg)
    verify_key_hex = "afa7d197c2d9e138d98a4c3e1265b85b8480412751264d17406a01bace73c578"
    verify_signature(key_hex=verify_key_hex, sig=sig, enc=enc)

    decrypted_data = decrypt_license(enc=enc, license_key=license_key)
    return decrypted_data


def read_license_file(path):
    try:
        with open(path) as f:
            return f.read()
    except (FileNotFoundError, PermissionError, OSError):
        raise OSError("License file not found") from None


def parse_license_payload(license_file):
    payload = license_file.replace("-----BEGIN LICENSE FILE-----\n", "").replace(
        "-----END LICENSE FILE-----\n", ""
    )
    try:
        return json.loads(base64.b64decode(payload))
    except (json.JSONDecodeError, base64.binascii.Error) as e:
        raise ValueError(
            f"Failed to decode license file {license_file}: {str(e)}"
        ) from None


def verify_algorithm(alg):
    if alg != "aes-256-gcm+ed25519":
        raise ValueError("License algorithm is not supported")


def verify_signature(key_hex, sig, enc):
    from nacl.encoding import HexEncoder
    from nacl.exceptions import BadSignatureError
    from nacl.signing import VerifyKey

    try:
        verify_key = VerifyKey(key=key_hex, encoder=HexEncoder)
        decoded_sig = base64.b64decode(s=sig)
        signed_content = f"license/{enc}".encode()

        if len(decoded_sig) != 64:
            raise ValueError("Signature verification failed: signature length is wrong")

        verify_key.verify(smessage=signed_content, signature=decoded_sig)
    except (AssertionError, BadSignatureError, ValueError) as e:
        raise ValueError(f"Signature verification failed: {str(e)}") from None


def decrypt_license(enc, license_key):
    from cryptography.exceptions import InvalidKey, InvalidTag
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    try:
        ciphertext, iv, tag = map(base64.b64decode, enc.split("."))
        digest = hashes.Hash(algorithm=hashes.SHA256(), backend=default_backend())
        digest.update(data=license_key.encode())
        key = digest.finalize()

        aes = Cipher(
            algorithm=algorithms.AES(key=key),
            mode=modes.GCM(initialization_vector=iv, tag=tag),
            backend=default_backend(),
        )

        dec = aes.decryptor()
        plaintext = dec.update(ciphertext) + dec.finalize()
        return json.loads(plaintext.decode())
    except (InvalidKey, InvalidTag):
        raise ValueError("Decryption failed: Invalid license key") from None


def is_running_in_jupyter():
    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":  # noqa: SIM103
            # Jupyter notebook or JupyterLab
            return True
        else:
            # Other environments
            return False
    except (ImportError, NameError):
        # Not running in IPython or Jupyter
        return False


class LicenseError(Exception):
    def __init__(self, message, filtered_traceback=None):
        self.filtered_traceback = filtered_traceback
        super().__init__(message)

    def __str__(self):
        if self.filtered_traceback:
            return (
                f"{self.args[0]}\n"
                "Traceback (most recent call last):\n"
                f"{self.filtered_traceback}"
            )
        return super().__str__()


def custom_exception_handler(
    exc_type=None, exc_value=None, exc_traceback=None, *args, **kwargs
):
    if is_running_in_jupyter():
        # Manually retrieve exception info in Jupyter,
        # because it handles them differently
        exc_type, exc_value, exc_traceback = sys.exc_info()

    if isinstance(exc_value, LicenseError):
        # Filter the traceback
        tb_lines = traceback.format_tb(exc_traceback)
        filtered_tb = []
        for line in tb_lines:
            # Skip lines with file details
            if not line.strip().startswith("File "):
                filtered_tb.append(line)

        # Combine filtered traceback
        filtered_traceback = "".join(filtered_tb)

        if is_running_in_jupyter():
            # For Jupyter Notebook, replace newlines with <br> for HTML
            from IPython.display import HTML, display

            filtered_traceback_html = filtered_traceback.replace("\n", "<br>")
            display(
                HTML(
                    f"<b>License Validation Error:</b> {exc_value.args[0]}<br>"
                    "<b>Traceback:</b>"
                    f"<br>{filtered_traceback_html}"
                )
            )
        else:
            # For standard Python interpreter, print normally
            custom_message = (
                f"{exc_value.args[0]}\n"
                "Traceback (most recent call last):\n"
                f"{filtered_traceback}"
            )
            print(custom_message)
    else:
        # Call the default hook for other exceptions or if exc_value is not an instance
        sys.__excepthook__(exc_type, exc_value, exc_traceback)


# Set the custom exception handler in Jupyter
if is_running_in_jupyter():
    from IPython.core.interactiveshell import InteractiveShell

    InteractiveShell.instance().set_custom_exc(
        (LicenseError,), custom_exception_handler
    )
else:
    # Set the custom excepthook globally for non-Jupyter environments
    sys.excepthook = custom_exception_handler


def raise_exception(message):
    try:
        raise LicenseError("License key error")
    except LicenseError:
        exc_type, exc_value, exc_tb = sys.exc_info()

        # Filter the traceback
        tb_lines = traceback.format_tb(exc_tb)
        filtered_tb = []
        for line in tb_lines:
            if not line.strip().startswith("File "):
                filtered_tb.append(line)

        filtered_traceback = "".join(filtered_tb)

        # Raise the exception again with the filtered traceback
        raise LicenseError(message, filtered_traceback) from None


def check_key(config, setup=False):
    license_from_env = os.getenv("COBALT_LICENSE_KEY")
    license_from_conf = config["license_key"]
    license_key = license_from_env if license_from_env else license_from_conf
    if license_key and license_key != DEFAULT_KEY:
        # try to check key offline
        check_license_result = check_offline_license()
        is_valid = check_license_result["valid"]
        if is_valid:
            data = get_data_from_offline_license(license_key)
        else:
            # check key online
            resp = get_license_data_by_key(license_key)
            data = resp.json()
            is_valid = data["meta"]["valid"]

        if is_valid:
            show_message = False
            if setup:
                license_key = data["data"]["attributes"]["key"]
                metadata = data["data"]["attributes"]["metadata"]

                expected_md_keys = ["name", "email", "company", "licenseType"]
                md = {
                    key if key != "licenseType" else "license_type": metadata.get(key)
                    for key in expected_md_keys
                }
                config["config"].update(md)
                config["license_key"] = license_key

        else:
            show_message = True
    else:
        show_message = True
    return config, show_message


def get_license_data_by_key(license_key):
    api_url = (
        "https://api.keygen.sh/v1/accounts/bluelightai/licenses/actions/validate-key"
    )
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }
    payload = {"meta": {"key": license_key}}
    response = requests.post(api_url, json=payload, headers=headers)
    return response

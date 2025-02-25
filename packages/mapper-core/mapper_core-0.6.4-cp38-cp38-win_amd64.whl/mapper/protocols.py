# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Protocol classes defining interfaces."""

from typing import Protocol

import numpy as np

from mapper.neighborgraph import KNNGraph


class CSRNeighborGraphLike(Protocol):
    _neighbors: np.ndarray
    _neighborhood_boundaries: np.ndarray
    _distances: np.ndarray


class NeighborGraphLike(Protocol):
    @property
    def raw_graph(self) -> KNNGraph:
        ...

    @property
    def graph(self) -> CSRNeighborGraphLike:
        ...


class SourceDataLike(Protocol):
    @property
    def X(self) -> np.ndarray:
        ...

    @property
    def shape(self) -> tuple:
        ...

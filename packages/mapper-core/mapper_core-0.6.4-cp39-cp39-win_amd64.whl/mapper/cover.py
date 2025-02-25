# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Classes representing covers and partitions of datasets."""
from typing import List

import numpy as np

from mapper import nerve
from mapper.matrix import MapperMatrix


class Cover:
    """A cover of a dataset.

    Maintains a link to the original dataset (as a MapperMatrix) and a list of
    arrays of integers, one for each set in the cover.
    """

    def __init__(self, dataset: MapperMatrix, sets: List[np.ndarray]):
        # we could validate that sets is actually a cover of dataset, but this
        # might be expensive
        self.dataset = dataset
        self.sets = sets
        self._edge_list = None

    def remapped_sets(self) -> List[List[int]]:
        return [self.dataset.translate_row_indices(u) for u in self.sets]


class Partition:
    """A partition of the points of a dataset.

    Maintains a link to the original dataset (as a MapperMatrix) and an array
    giving assignments of each point to an integer identifying a set in the
    partition.
    """

    def __init__(self, dataset: MapperMatrix, membership_vec: np.ndarray):
        if len(membership_vec.shape) != 1:
            raise ValueError("membership_vec must be 1-dimensional")
        if dataset.X.shape[0] != membership_vec.shape[0]:
            raise ValueError(
                "membership_vec must have the same number of points as dataset"
            )
        self.dataset = dataset
        self.membership_vec = membership_vec.astype(np.int32, order="C", copy=False)

    def as_cover(self) -> Cover:
        """Reinterpret this partition as a Cover."""
        sets = list(nerve.partition_vec_to_cover(self.membership_vec))
        return Cover(self.dataset, sets)

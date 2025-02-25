# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Classes related to data matrices for use with our Mapper implementation."""

from typing import Optional, Union

import msgpack
import numpy as np
import pandas as pd
import scipy.sparse


class MapperMatrix:
    """Represents a data matrix for use with the Mapper class.

    Mostly a thin wrapper around a dense or sparse array.

    """

    _serialization_version = 2

    def __init__(
        self,
        matrix: Union[
            np.ndarray, pd.DataFrame, scipy.sparse.csr_array, scipy.sparse.csr_matrix
        ],
        data_id: Optional[str] = None,
    ):
        """Initialize a MapperMatrix.

        Params:
            matrix: An array-like object with the data
            data_id: An optional id used to identify data sources when (de)serializing.
        """

        if not isinstance(
            matrix, (np.ndarray, scipy.sparse.csr_array, scipy.sparse.csr_matrix)
        ):
            matrix = np.array(matrix)
        if len(matrix.shape) != 2:
            raise ValueError(
                f"Input array must be two-dimensional. Shape is {matrix.shape}"
            )
        self._X = matrix.astype(np.float32)
        self.data_id = data_id

    @property
    def X(self) -> np.ndarray:
        """The data stored in the matrix."""
        return self._X

    @property
    def shape(self) -> tuple:
        """Return the shape of the data matrix."""

        return self._X.shape

    def to_msgpack(self) -> bytes:
        """Save all parameters to a msgpack object.

        Note that this does not currently store the data matrix itself."""

        data = {
            "obj_type": "MapperMatrix",
            "version": self._serialization_version,
            "data_id": self.data_id,
        }

        return msgpack.packb(data)  # type: ignore

    # since self._X is not stored, there's no reason to deserialize this

    def __repr__(self) -> str:
        """Return the string representation of this MapperMatrix."""
        return f"MapperMatrix(shape={self.shape})"

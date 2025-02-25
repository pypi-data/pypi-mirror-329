# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++
"""Custom exceptions for mapper-core."""


class SerializationError(Exception):
    """Error raised when serialization or deserialization fails."""

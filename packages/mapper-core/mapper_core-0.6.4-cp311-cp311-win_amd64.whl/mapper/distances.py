# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Tools for managing distance functions."""
from typing import Callable, Union

from pynndescent.distances import named_distances


def _get_metric_fn(metric: Union[str, Callable]) -> Callable:
    """Helper to get a callable metric function from unvalidated input."""
    if isinstance(metric, str):
        if metric in named_distances:
            metric = named_distances[metric]
        else:
            raise ValueError(f"Metric {metric} is not supported")

    return metric

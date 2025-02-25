import io

import numpy as np


def np_to_bytes(arr: np.ndarray) -> bytes:
    with io.BytesIO() as buf:
        np.save(buf, arr, allow_pickle=False)
        buf.seek(0)
        data = buf.read()
    return data


def np_from_bytes(data: bytes) -> np.ndarray:
    with io.BytesIO(data) as buf:
        arr = np.load(buf, allow_pickle=False)
    return arr


def default_encode(obj):
    if isinstance(obj, np.ndarray):
        return {"__class__": "ndarray", "as_bytes": np_to_bytes(obj)}
    return obj


def object_hook(obj):
    if obj.get("__class__") == "ndarray":
        return np_from_bytes(obj["as_bytes"])
    return obj

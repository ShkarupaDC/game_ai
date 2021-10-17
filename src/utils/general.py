import numpy as np
import inspect
from typing import Any, Callable, Union


def normalize(
    mapping: dict[str, float], softmax: bool = False
) -> dict[str, float]:
    keys, values = zip(*mapping.items())

    values = np.array(values)
    if softmax is True:
        values = np.exp(values - np.max(values))
    values = values / np.sum(values)

    normalized = dict(zip(keys, values.tolist()))
    return normalized


def sample(dist: dict[int, float], count: int = 1) -> Union[int, list[int]]:
    values, probs = zip(*dist.items())
    actions = np.random.choice(values, size=count, replace=False, p=probs)
    actions = actions.tolist()
    return actions[0] if len(actions) == 1 else actions


def color_to_vector(color: str) -> list[float]:
    part_len, base = 2, 16
    rgb = [
        color[idx : idx + part_len] for idx in range(1, len(color), part_len)
    ]
    mapping = lambda color: int(color, base) / 2 ** base
    return list(map(mapping, rgb))


def nearest_odd(value: int) -> int:
    return value + 1 if value % 2 == 0 else value


def sort_dict(
    mapping: dict[Any, Any], by_value: bool = False
) -> dict[Any, Any]:
    mapping = dict(
        sorted(mapping.items(), key=lambda pair: pair[1 if by_value else 0])
    )
    return mapping


def get_arg_names(fn: Callable) -> list[str]:
    return list(inspect.signature(fn).parameters.keys())

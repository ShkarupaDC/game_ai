import time
import random
from functools import wraps
from collections import Counter
from typing import Any, Callable, Union


def normalize(counter: dict[str, float]) -> dict[str, float]:
    if isinstance(counter, Counter):
        counter = dict(counter)
    sum_all = sum(counter.values())
    normalized = {key: value / sum_all for key, value in counter.items()}
    return normalized


def sample(dist: dict[int, float], count: int = 1) -> Union[int, list[int]]:
    values, probs = zip(*dist.items())
    actions = random.choices(
        population=values,
        weights=probs,
        k=count,
    )
    return actions[0] if len(actions) == 1 else actions


def color_to_vector(color: str) -> list[float]:
    part_len, base = 2, 16
    rgb = [
        color[idx : idx + part_len] for idx in range(1, len(color), part_len)
    ]
    mapping = lambda color: int(color, base) / 2 ** base
    return list(map(mapping, rgb))


def copy_interface(parent: object, child: object, attrs: list[str]) -> object:
    for name in attrs:
        attribute = getattr(parent, name)
        setattr(child, name, attribute)
    return child


def time_it(stdout: bool = False) -> Callable:
    def timer(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()

            if stdout is True:
                print(f"Time ({function.__name__}):", end - start)
            return result

        return wrapper

    return timer


def bitwise_or(xs: list[bool], ys: list[bool]) -> list[bool]:
    return [x or y for x, y in zip(xs, ys)]
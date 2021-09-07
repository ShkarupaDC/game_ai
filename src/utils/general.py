import random
from collections import Counter


def normalize(counter: dict[str, float]) -> dict[str, float]:
    if isinstance(counter, Counter):
        counter = dict(counter)
    sum_all = sum(counter.values())
    normalized = {}
    for key, value in counter.items():
        normalized[key] = value / sum_all
    return normalized


def sample(dist: dict[str, float]) -> str:
    actions = random.choices(
        population=list(dist.keys()),
        weights=list(dist.values()),
    )
    return actions[0]


def format_color(r: float, g: float, b: float) -> str:
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def color_to_vector(color: list[int]) -> list[float]:
    return list(
        map(
            lambda x: int(x, 16) / 256.0,
            [color[1:3], color[3:5], color[5:7]],
        )
    )

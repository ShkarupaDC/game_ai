from typing import Any


def make_2d_grid(size: tuple[int, int], value: Any) -> list[list[Any]]:
    height, width = size
    return [[value] * width for _ in range(height)]

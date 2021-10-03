from typing import Union

from ..utils.vector import Vector

Position = Vector
Action = int
Cost = Union[int, float]
AdjList = dict[int, list[tuple[int, Cost]]]
TextMaze = list[list[str]]

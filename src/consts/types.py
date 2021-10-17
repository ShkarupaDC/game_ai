import numpy as np
from typing import Union, Optional, Any

from ..utils.vector import Vector

Position = Vector
Action = int
Cost = Union[int, float]
AdjList = dict[int, list[tuple[int, Cost]]]
AdjMatrix = np.ndarray
PosToIdx = dict[Position, int]
TextMaze = list[list[str]]
GameResult = dict[str, Optional[Any]]

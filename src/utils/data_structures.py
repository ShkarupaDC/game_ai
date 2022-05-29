import numpy as np
import heapq
from collections import deque
from typing import Any, Optional, Union
from dataclasses import dataclass

from ..consts.types import PosToIdx, Position, Cost


class Queue:
    def __init__(self) -> None:
        self.data = deque()

    def push(self, value: Any) -> None:
        self.data.append(value)

    def pop(self) -> Any:
        return self.data.popleft()

    def is_empty(self) -> bool:
        return len(self.data) == 0


class Stack:
    def __init__(self) -> None:
        self.data = deque()

    def push(self, value: Any) -> None:
        self.data.append(value)

    def pop(self) -> Any:
        return self.data.pop()

    def is_empty(self) -> bool:
        return len(self.data) == 0


class PriorityQueue:
    def __init__(self) -> None:
        self.queue = []

    def push(self, item: Any, priority: Union[int, float]) -> None:
        heapq.heappush(self.queue, (priority, item))

    def pop(self) -> tuple[Any, Union[int, float]]:
        priority, item = heapq.heappop(self.queue)
        return item, priority

    def is_empty(self) -> bool:
        return len(self.queue) == 0


@dataclass(eq=False)
class MazeDistance:
    maze_dists: np.ndarray
    mapping: PosToIdx
    goal_mapping: Optional[dict[int, int]]

    def get(self, start: Position, end: Position) -> Cost:
        end = self.mapping[end]
        if self.goal_mapping is not None:
            end = self.goal_mapping[end]
        start = self.mapping[start]
        return self.maze_dists[end, start]

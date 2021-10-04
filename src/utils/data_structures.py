import numpy as np
import heapq
from collections import deque
from typing import Any, Union
from dataclasses import dataclass

from ..consts.types import Position, Cost


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
class DistanceMemory:
    dist: np.ndarray
    mapping: dict[Position, int]
    goal_idxs: dict[int, int]

    def get(self, start: Position, end: Position) -> Cost:
        i_idx = self.goal_idxs[self.mapping[end]]
        j_idx = self.mapping[start]
        return self.dist[i_idx, j_idx]


class IndexDict:
    def __init__(self) -> None:
        self.idx = 0
        self.data = dict()

    def __getitem__(self, position: Position) -> int:
        idx = self.data.get(position, self.idx)
        if idx == self.idx:
            self.idx = idx + 1
            self.data[position] = idx
        return idx

    def as_dict(self) -> dict[Position, int]:
        return self.data

import heapq
from collections import deque
from typing import Any, Union


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

import numpy as np
from collections import defaultdict
from dataclasses import dataclass, field

from .data_structures import Queue
from .graph import adjlist_to_adjmatrix
from ..consts.direction import TO_VECTOR, Direction
from ..consts.types import AdjList, AdjMatrix, PosToIdx, Position


@dataclass(eq=False)
class Grid:
    data: np.ndarray
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self) -> None:
        self.width, self.height = self.data.shape

    def __getitem__(self, idx: int) -> bool:
        return self.data[idx]

    def __setitem__(self, key: int, item: bool) -> None:
        self.data[key] = item

    def get_positions(self) -> list[Position]:
        xs, ys = np.nonzero(self.data == True)
        return [Position(x, y) for x, y in zip(xs, ys)]

    def invert(self) -> "Grid":
        return Grid(~self.data)

    def count(self, value: bool = True) -> int:
        return (self.data == value).sum()

    @classmethod
    def full(cls, width: int, height: int, value: bool = False) -> "Grid":
        data = np.full((width, height), value)
        return cls(data)


@dataclass(eq=False)
class Walls(Grid):
    def get_neighbors(self, position: Position) -> list[Position]:
        neighbors = []
        for action, move in TO_VECTOR.items():
            if action != Direction.STOP:
                next = (position + move).as_int()
                if not self.data[next.x][next.y]:
                    neighbors.append(next)
        return neighbors

    def get_adjlist(self) -> AdjList:
        adjlist = defaultdict(list)
        visited = set()

        for start in self.invert().get_positions():
            queue = Queue()
            queue.push(start)

            while not queue.is_empty():
                parent = queue.pop()
                if parent in visited:
                    continue
                visited.add(parent)

                for neighbor in self.get_neighbors(parent):
                    queue.push(neighbor)
                    adjlist[parent].append((neighbor, 1))
        return adjlist

    def get_adjmatrix(self) -> tuple[AdjMatrix, PosToIdx]:
        adjlist = self.get_adjlist()
        return adjlist_to_adjmatrix(adjlist)

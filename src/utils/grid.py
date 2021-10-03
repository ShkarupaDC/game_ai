import numpy as np
from dataclasses import dataclass

from ..consts.types import Position


@dataclass(eq=False)
class Grid:
    data: np.ndarray

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

    @staticmethod
    def full(width: int, height: int, value: bool = False) -> "Grid":
        data = np.full((width, height), value)
        return Grid(data)

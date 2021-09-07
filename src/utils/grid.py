import numpy as np
from dataclasses import dataclass


@dataclass(eq=False)
class Grid:
    width: int
    height: int
    value: bool = False

    def __post_init__(self) -> None:
        self.data = np.full((self.width, self.height), self.value)

    def __getitem__(self, idx: int) -> bool:
        return self.data[idx]

    def __setitem__(self, key: int, item: bool) -> None:
        self.data[key] = item

    def count(self, value: bool = True) -> int:
        return (self.data == value).sum()

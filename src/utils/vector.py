import math
from dataclasses import dataclass
from typing import Generator, Union


@dataclass(order=True, unsafe_hash=True)
class Vector:
    x: float = 0.0
    y: float = None
    threshold: float = 1e-6

    def __post_init__(self) -> None:
        if self.y is None:
            self.y = self.x

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def as_int(self, up: bool = False) -> "Vector":
        if up is True:
            return Vector(
                int(self.x + 0.5),
                int(self.y + 0.5),
            )
        return Vector(int(self.x), int(self.y))

    def manhattan(self, other: "Vector") -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def nearest(self) -> "Vector":
        return self.as_int(up=True)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(
            self.x + other.x,
            self.y + other.y,
        )

    def __mul__(self, scalar: Union[int, float]) -> "Vector":
        return Vector(
            self.x * scalar,
            self.y * scalar,
        )

    def __eq__(self, other: "Vector") -> bool:
        if abs(self.x - other.x) < self.threshold:
            if abs(self.y - other.y) < self.threshold:
                return True
        return False

    def __iter__(self) -> Generator[float, None, None]:
        for coord in self.as_tuple():
            yield coord

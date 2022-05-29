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
        dx, dy = abs(self - other)
        return dx + dy

    def chebyshev(self, other: "Vector") -> float:
        dx, dy = abs(self - other)
        return min(dx, dy)

    def euclidean(self, other: "Vector") -> float:
        dx2, dy2 = (self - other) ** 2
        return dx2 + dy2

    def nearest(self) -> "Vector":
        return self.as_int(up=True)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scalar: Union[int, float]) -> "Vector":
        return Vector(
            self.x * scalar,
            self.y * scalar,
        )

    def __floordiv__(self, value: Union[int, float]) -> "Vector":
        return (self / value).as_int()

    def __truediv__(self, value: Union[int, float]) -> "Vector":
        if value == 0:
            raise Exception("Division by zero")
        return Vector(
            self.x / value,
            self.y / value,
        )

    def __pow__(self, value: float) -> "Vector":
        return Vector(
            self.x ** value,
            self.y ** value,
        )

    def __abs__(self) -> "Vector":
        return Vector(
            abs(self.x),
            abs(self.y),
        )

    def __eq__(self, other: "Vector") -> bool:
        if abs(self.x - other.x) < self.threshold:
            if abs(self.y - other.y) < self.threshold:
                return True
        return False

    def __iter__(self) -> Generator[float, None, None]:
        for coord in self.as_tuple():
            yield coord

from dataclasses import dataclass
from typing import Optional

from ..consts.direction import *
from ..utils.grid import Grid
from ..utils.vector import Vector


class Agent:
    def __init__(self, index: int = 0) -> None:
        self.index = index

    def get_action(self, state) -> int:
        raise NotImplementedError


@dataclass(eq=False)
class Configuration:
    position: Vector
    direction: int

    def get_position(self) -> Vector:
        return self.position

    def get_direction(self) -> int:
        return self.direction

    def generate_next(self, vector: Vector) -> "Configuration":
        direction = Actions.vector_to_direction(vector)
        if direction == Direction.STOP:
            direction = self.direction
        return Configuration(self.position + vector, direction)


@dataclass(eq=False)
class AgentState:
    configuration: Configuration
    is_pacman: bool
    scared_timer: int = 0

    def __post_init__(self) -> None:
        self.start = self.configuration

    def get_position(self) -> Optional[Vector]:
        if self.configuration == None:
            return None
        return self.configuration.get_position()

    def get_direction(self) -> int:
        return self.configuration.get_direction()


class Actions:
    EPS = 1e-3

    @staticmethod
    def get_possible_actions(config: Configuration, walls: Grid) -> list[int]:
        xy = config.get_position()
        xy_int = xy.as_int(True)

        if xy.manhattan(xy_int) > Actions.EPS:
            return [config.get_direction()]

        actions = []
        for direction, vector in TO_VECTOR.items():
            x, y = (xy_int + vector).as_tuple()
            if not walls[x][y]:
                actions.append(direction)

        return actions

    @staticmethod
    def reverse_direction(action: int) -> int:
        return -action

    @staticmethod
    def vector_to_direction(vector: Vector) -> int:
        dx, dy = vector
        if dy > 0:
            return Direction.NORTH
        if dy < 0:
            return Direction.SOUTH
        if dx < 0:
            return Direction.WEST
        if dx > 0:
            return Direction.EAST
        return Direction.STOP

    @staticmethod
    def direction_to_vector(direction: int, speed: float = 1.0) -> Vector:
        return TO_VECTOR[direction] * speed

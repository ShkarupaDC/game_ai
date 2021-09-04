import numpy as np

from .const import *


class PostionState:
    def __init__(
        self, position: tuple[float, float], direction: tuple[int, int]
    ) -> None:
        self.position = position
        self.direction = direction

    def generate_next(self, change: tuple[float, float]) -> "PostionState":
        x, y = self.position
        dx, dy = change

        direction = Action.change_to_direction(change)
        if direction == STOP:
            direction = self.direction

        next_x, next_y = x + dx, y + dy
        return PostionState((next_x, next_y), direction)

    def get_position(self) -> tuple[float, float]:
        return self.position

    def get_direction(self) -> int:
        return self.direction


class AgentState:
    def __init__(self, position_state: PostionState, is_pacman: bool) -> None:
        self.position_state = position_state
        self.is_pacman = is_pacman

    def get_position(self) -> tuple[float, float]:
        self.position_state.get_position()

    def get_direction(self) -> int:
        self.position_state.get_direction()


class Agent:
    def __init__(self, index: int = 0) -> None:
        self.index = index

    def get_action(self, state: AgentState) -> int:
        raise NotImplementedError


class Action:
    @staticmethod
    def reverse_direction(direction: int) -> int:
        return -direction

    @staticmethod
    def get_allowed_action(
        position_state: PostionState, walls: np.ndarray
    ) -> list[int]:
        x, y = position_state.get_position()
        x_int = int(x + 0.5)
        y_int = int(y + 0.5)

        if abs(x - x_int) + abs(y - y_int) > EPS:
            return [position_state.get_direction()]

        height, width = walls.shape
        directions = []

        for direction, (dx, dy) in DIRECTIONS.items():
            next_x = x_int + dx
            next_y = y_int + dy

            if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height:
                continue
            if not walls[next_y, next_x]:
                directions.append(direction)

        return directions

    @staticmethod
    def change_to_direction(change: tuple[float, float]) -> int:
        dx, dy = change
        if dy < 0:
            return NORTH
        if dy > 0:
            return SOUTH
        if dx < 0:
            return WEST
        if dx > 0:
            return EAST
        return STOP

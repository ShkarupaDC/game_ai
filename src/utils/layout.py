import numpy as np
from pathlib import Path
from typing import Optional, Union

from .grid import Grid
from ..utils.vector import Vector


class Layout:
    def __init__(self, maze: list[list[str]]) -> None:
        self.maze = np.array(maze)
        self.height, self.width = self.maze.shape
        self.walls = Grid(self.width, self.height)
        self.food = Grid(self.width, self.height)
        self.capsules = []
        self.agent_positions = []
        self.num_ghosts = 0
        self.__process_maze()
        self.total_food = self.food.count()

    def get_num_ghosts(self) -> int:
        return self.num_ghosts

    def __process_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                value = self.maze[self.height - (y + 1)][x]
                position = Vector(x, y)
                self.__process_point(position, value)

    def __process_point(self, position: Vector, value: str) -> None:
        x, y = position
        if value == "#":
            self.walls[x][y] = True
        elif value == ".":
            self.food[x][y] = True
        elif value == "o":
            self.capsules.append(position)
        elif value == "P":
            self.agent_positions.append((True, position))
        elif value in ["1", "2", "3", "4"]:
            self.num_ghosts += 1
            self.agent_positions.append((False, position))

    @staticmethod
    def get_layout(name: str, layout_dir: str = "assets/layouts") -> "Layout":
        layout_dir = Path(layout_dir)
        name = name if name.endswith(".lay") else f"{name}.lay"
        layout = Layout.load_layout(layout_dir / name)
        return layout

    @staticmethod
    def load_layout(path: Union[str, Path]) -> Optional["Layout"]:
        if not Path(path).exists():
            return None
        try:
            with open(path, mode="r") as file:
                maze = [list(line.strip()) for line in file]
            return Layout(maze)
        except:
            return None

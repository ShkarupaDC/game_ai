import numpy as np
from pathlib import Path
from typing import Optional


class Layout:
    def __init__(self, maze: list[list[str]]) -> None:
        self.maze = np.array(maze)
        self.height, self.width = self.maze.shape
        self.walls = np.full_like(
            self.maze,
            fill_value=False,
            dtype="bool",
        )
        self.food = np.full_like(
            self.maze,
            fill_value=False,
            dtype="bool",
        )
        self.agent_positions = []
        self.__process_maze()

    def __process_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.__process_maze_point(self.maze[y, x], x, y)
        self.agent_positions.sort()

    def __process_maze_point(self, point: str, x: int, y: int) -> None:
        if point == "#":
            self.walls[y, x] = True
        elif point == ".":
            self.food[y, x] = True
        elif point == "P":
            self.agent_positions.append((0, (x, y)))

    @staticmethod
    def load_layout(path: str) -> Optional["Layout"]:
        path = Path(path)
        if path.exists() and path.suffix == ".lay":
            try:
                with open(path, mode="r") as file:
                    maze = [list(line.strip()) for line in file]
                return Layout(maze)
            except:
                return None
        return None

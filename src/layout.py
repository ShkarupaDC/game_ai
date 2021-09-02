from pathlib import Path
from typing import Optional

from .utils import make_2d_grid


class Layout:
    def __init__(self, maze: list[list[str]]) -> None:
        self.width = len(maze[0])
        self.height = len(maze)
        self.walls = make_2d_grid((self.height, self.width), False)
        self.food = make_2d_grid((self.height, self.width), False)
        self.agent_positions = []
        self.__process_maze(maze)

    def __process_maze(self, maze: list[list[str]]) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.__process_maze_point(maze[y][x], x, y)
        self.agent_positions.sort()

    def __process_maze_point(self, point: str, x: int, y: int) -> None:
        if point == "#":
            self.walls[y][x] = True
        elif point == ".":
            self.food[y][x] = True
        elif point == "P":
            self.agent_positions.append((0, (x, y)))

    @staticmethod
    def load_layout(path: str) -> Optional["Layout"]:
        path = Path(path)
        if path.exists() and path.suffix == ".lay":
            try:
                with open(path, mode="r") as file:
                    maze = [line.strip() for line in file]
                return Layout(maze)
            except:
                return None
        return None

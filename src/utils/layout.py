import numpy as np
from pathlib import Path
from typing import Any, Optional, Union
from dataclasses import InitVar, dataclass, field

from .grid import Grid
from ..consts.types import Position, TextMaze


@dataclass(eq=False)
class Layout:
    height: int
    width: int
    walls: InitVar[Optional[Grid]] = None
    food: InitVar[Optional[Grid]] = None
    capsules: list[Position] = field(default_factory=list)
    agent_positions: list[tuple[bool, Position]] = field(default_factory=list)
    num_ghosts: int = 0

    def __post_init__(
        self, food: Optional[Grid], walls: Optional[Grid]
    ) -> None:
        self.food = (
            food
            if self.food is not None
            else Grid.full(self.width, self.height)
        )
        self.walls = (
            walls
            if self.walls is not None
            else Grid.full(self.width, self.height)
        )

    @staticmethod
    def from_text(name: str, maze_dir: str = "assets/layouts") -> "Layout":
        layout = MazeParser.parse(name, maze_dir)
        return layout

    @staticmethod
    def generate(*maze_args: Any, **maze_kwargs: Any) -> "Layout":
        layout = MazeGenerator.generate(*maze_args, **maze_kwargs)
        return layout


class MazeParser:
    @staticmethod
    def parse(name: str, maze_dir: str) -> Layout:
        maze = MazeParser.__get_maze(name, maze_dir)
        height, width = maze.shape
        layout = Layout(height, width)
        MazeParser.__process_maze(maze, layout)
        return layout

    @staticmethod
    def __process_maze(maze: TextMaze, layout: Layout) -> None:
        for y in range(layout.height):
            for x in range(layout.width):
                value = maze[layout.height - (y + 1)][x]
                position = Position(x, y)
                MazeParser.__process_point(layout, position, value)

    @staticmethod
    def __process_point(
        layout: Layout, position: Position, value: str
    ) -> None:
        x, y = position
        if value == "#":
            layout.walls[x][y] = True
        elif value == ".":
            layout.food[x][y] = True
        elif value == "o":
            layout.capsules.append(position)
        elif value == "P":
            layout.agent_positions.append((True, position))
        elif value in ["1", "2", "3", "4"]:
            layout.num_ghosts += 1
            layout.agent_positions.append((False, position))

    @staticmethod
    def __get_maze(name: str, maze_dir: str) -> Optional[TextMaze]:
        maze_dir = Path(maze_dir)
        name = name if name.endswith(".lay") else f"{name}.lay"
        maze = MazeParser.__load_maze(maze_dir / name)
        return maze

    @staticmethod
    def __load_maze(path: Union[str, Path]) -> Optional[TextMaze]:
        if not Path(path).exists():
            return None
        try:
            with open(path, mode="r") as file:
                return np.array([list(line.strip()) for line in file])
        except:
            return None


class MazeGenerator:
    @staticmethod
    def generate(
        height: int,
        width: int,
        nethod: str,
        num_ghosts: int,
        num_food: int,
        num_capsules: int,
    ) -> Layout:
        layout = Layout(height, width)
        return layout

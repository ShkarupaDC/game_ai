from typing import Callable

from .rules import GameState
from .agent import Actions
from .search_solvers import bfs, dfs, ucs
from ..consts.types import Position, Cost
from ..consts.direction import Direction
from ..consts.graphics import Key


class GhostSearch:
    def __init__(
        self,
        ghost_idxs: list[int],
        cost_fn: Callable = lambda _: 1,
    ) -> None:
        self.ghost_idxs = ghost_idxs
        self.cost_fn = cost_fn

    def update(self, game_state: GameState) -> None:
        self.walls = game_state.get_walls()
        self.goals = [
            game_state.get_ghost_position(idx) for idx in self.ghost_idxs
        ]
        self.start = game_state.get_pacman_position()

    def get_start(self) -> Position:
        return self.start

    def get_goals(self) -> list[Position]:
        return self.goals

    def get_neighbors(self, position: Position) -> list[tuple[Position, Cost]]:
        neighbors = []
        for action in Direction.as_list():
            vector = Actions.direction_to_vector(action)

            next = (position + vector).as_int()
            x, y = next
            if not self.walls[x][y]:
                cost = self.cost_fn(next)
                neighbors.append((next, cost))

        return neighbors

    def in_goals(self, position: Position) -> list[bool]:
        return [goal == position for goal in self.goals]


class GhostSearchProblem:
    def __init__(
        self,
        problem: GhostSearch,
        search_fns: list[Callable] = [bfs, dfs, ucs],
        key: str = Key.Z,
    ) -> None:
        self.fns, self.idx = search_fns, 0
        self.key = key
        self.last_keys = []
        self.problem = problem
        self.paths = None

    def update(self, state: GameState) -> None:
        self.problem.update(state)

        keys = state.keys_pressed()
        if self.key in keys:
            if not self.key in self.last_keys:
                self.idx = (self.idx + 1) % len(self.fns)
        self.last_keys = keys

        fn = self.fns[self.idx]
        self.paths = list(zip(self.problem.ghost_idxs, fn(self.problem)))

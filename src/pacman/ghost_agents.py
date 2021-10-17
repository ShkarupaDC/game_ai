from collections import Counter
from functools import partial
from typing import Callable

from .search.problems import PositionProblem, SearchProblem
from .search.heuristics import distance_heuristic
from .search.solvers import a_star
from .game import Agent
from .rules import GameState
from ..consts.direction import Direction
from ..consts.types import Action
from ..pacman.agent import Actions
from ..utils.general import normalize, sample


class GhostAgent(Agent):
    def __init__(self, index: int) -> None:
        self.index = index

    def get_action(self, state: GameState) -> int:
        dist = self.get_distribution(state)
        if len(dist) == 0:
            return Direction.STOP
        return sample(dist)

    def get_distribution(self, state: GameState) -> dict[int, float]:
        raise NotImplementedError


class RandomGhost(GhostAgent):
    def get_distribution(self, state: GameState) -> dict[int, float]:
        dist = Counter(state.get_legal_actions(self.index))
        return normalize(dict(dist))


SearchFn = Callable[[SearchProblem], list[Action]]


class GreedyGhost(GhostAgent):
    def __init__(
        self,
        index: int,
        search_fn: SearchFn = partial(
            a_star, heuristic=distance_heuristic, greedy=True
        ),
    ) -> None:
        super().__init__(index=index)
        self.search_fn = search_fn

    def get_distribution(self, state: GameState) -> dict[int, float]:
        ghost = state.get_ghost_position(self.index)
        dist = dict()

        pacman = state.get_pacman_position()
        for action in state.get_legal_actions(self.index):

            move = Actions.direction_to_vector(action)
            next_position = ghost + move

            problem = PositionProblem(state, pacman, next_position)
            actions = self.search_fn(problem)

            dist[action] = -len(actions)

        return normalize(dist, softmax=True)

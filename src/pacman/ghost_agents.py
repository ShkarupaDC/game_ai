from collections import Counter

from ..consts.direction import Direction
from .game import Agent
from .rules import GameState
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
        return normalize(dist)

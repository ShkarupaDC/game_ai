import random

from ..consts.direction import Directions
from .game import Agent


class KeyboardAgent(Agent):
    def __init__(self, index: int = 0) -> None:
        self.last_move = Directions.STOP
        self.index = index
        self.keys = []

    def get_action(self, state) -> str:
        keys = list(state.keys_waiting()) + list(state.keys_pressed())
        if len(keys) > 0:
            self.keys = keys

        legal = state.get_legal_actions(self.index)
        move = self.get_move(legal)

        if move == Directions.STOP:
            if self.last_move in legal:
                move = self.last_move

        if move not in legal:
            move = random.choice(legal)

        self.last_move = move
        return move

    def get_move(self, legal: list[int]) -> int:
        move = Directions.STOP
        if "Left" in self.keys and Directions.WEST in legal:
            move = Directions.WEST
        if "Right" in self.keys and Directions.EAST in legal:
            move = Directions.EAST
        if "Up" in self.keys and Directions.NORTH in legal:
            move = Directions.NORTH
        if "Down" in self.keys and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move

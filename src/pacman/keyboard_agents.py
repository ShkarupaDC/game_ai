import random

from .game import Agent
from ..graphics.ui import UI
from ..consts.direction import Direction
from ..consts.graphics import Key


class KeyboardAgent(Agent):
    def __init__(self, index: int = 0) -> None:
        self.last_move = Direction.STOP
        self.index = index
        self.keys = []

    def get_action(self, state) -> str:
        keys = set(UI.keys_waiting() + UI.keys_pressed())
        if len(keys) > 0:
            self.keys = keys

        legal = state.get_legal_actions(self.index)
        move = self.get_move(legal)

        if move == Direction.STOP:
            if self.last_move in legal:
                move = self.last_move

        if move not in legal:
            move = random.choice(legal)

        self.last_move = move
        return move

    def get_move(self, legal: list[int]) -> int:
        move = Direction.STOP
        if Key.LEFT in self.keys and Direction.WEST in legal:
            move = Direction.WEST
        if Key.RIGHT in self.keys and Direction.EAST in legal:
            move = Direction.EAST
        if Key.UP in self.keys and Direction.NORTH in legal:
            move = Direction.NORTH
        if Key.DOWN in self.keys and Direction.SOUTH in legal:
            move = Direction.SOUTH
        return move

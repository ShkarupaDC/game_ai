from dataclasses import dataclass

from ..rules import GameState
from ...consts.types import Action


@dataclass(eq=False)
class ReflexState:
    game_state: GameState
    agent: int = 0
    depth: int = 0

    @property
    def action(self) -> Action:
        return self.game_state.get_last_action()

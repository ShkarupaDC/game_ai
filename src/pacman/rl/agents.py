import numpy as np
from typing import Optional

from .config import DQNAgentConfig
from .dqn.model import Model
from .dqn.utils.experience import Experience
from ..rules import GameState
from ..agent import Agent
from ...consts.direction import Direction
from ...consts.types import Action


ACTION_MAP = {
    0: Direction.NORTH,
    1: Direction.WEST,
    2: Direction.SOUTH,
    3: Direction.EAST,
}

INVERSE_ACTION_MAP = {value: key for key, value in ACTION_MAP.items()}


class DQNAgent(Agent):
    def __init__(self, config: DQNAgentConfig) -> None:
        self.config = config
        self.model = Model(config.model)
        self.eps = config.eps_params.start
        self.step: int = 0
        self.index: int = 0

        self.state: np.ndarray
        self.last_state: np.ndarray
        self.reward: float
        self.action: int
        self.score: float
        self.terminal: bool
        self.q_values: list[float]

    def register_state(self, state: GameState) -> None:
        self.model.load_checkpoint()
        self.state = self.__get_env_state(state)
        self.last_state = None
        self.reward = 0
        self.action = None
        self.score = state.get_score()
        self.terminal = False
        self.q_values = []

    def __observe_state(self, state: GameState) -> None:
        if self.action is not None:
            score = state.get_score()
            self.reward = score - self.score
            self.score = score

            self.last_state = self.state.copy()
            self.state = self.__get_env_state(state)

            if self.config.train:
                experience = Experience(
                    self.last_state,
                    self.action,
                    self.state,
                    self.reward,
                    self.terminal,
                )
                self.model.train(experience)
        self.step += 1
        if self.config.train:
            self.__update_eps()

    def __update_eps(self) -> None:
        eps = self.config.eps_params
        # ratio = 1 / np.exp(self.step / eps.decay)
        scale = eps.start - eps.end
        # self.eps = eps.end + scale * ratio
        self.eps = eps.end + scale * (1 - self.model.step / eps.step)

    def get_action(self, state: GameState) -> Action:
        self.terminal = False
        self.__observe_state(state)

        action = self.__get_action(state)
        if action not in state.get_legal_actions(self.index):
            action = Direction.STOP
        return action

    def __get_action(self, state: GameState) -> Action:
        if np.random.rand() > self.eps:
            values = self.model.evaluate(self.state)
            max_value = values.max()
            self.q_values.append(max_value)

            action = np.argwhere(values == max_value).flatten()
            if len(action) > 1:
                action = np.random.choice(action)
            action = action.item()
        else:
            legal = [
                action
                for action in state.get_legal_actions(self.index)
                if action != Direction.STOP
            ]
            action = INVERSE_ACTION_MAP[np.random.choice(legal)]
        self.action = action
        return ACTION_MAP[action]

    def __get_env_state(self, state: GameState) -> np.ndarray:
        matrices = [
            state.get_pacman_matrix(),
            state.get_ghost_matrix(),
            state.get_food().data,
            state.get_walls().data,
        ]
        return np.stack(matrices).astype(np.float32)

    def final(self, state: GameState) -> None:
        self.terminal = True
        self.__observe_state(state)
        self.model.save_checkpoint()
        print(
            "Step:", self.step, "Max Q value:", max(self.q_values, default=0)
        )

    def get_algo(self) -> Optional[str]:
        return "dqn"

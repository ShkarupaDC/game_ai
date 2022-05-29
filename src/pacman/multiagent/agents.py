from functools import partial
from typing import Callable, Generator, Optional
from dataclasses import dataclass, field

from .states import ReflexState
from .utilities import utility_fn
from ..agent import Agent
from ..rules import GameState
from ...consts.game import INF_COST
from ...consts.types import Action, Cost
from ...consts.direction import Direction
from ...utils.graph import get_maze_dists
from ...utils.general import get_arg_names

StateGenerator = Generator[ReflexState, None, None]
UtilityFn = Callable[[ReflexState], Cost]


@dataclass(order=True)
class Value:
    cost: Cost = 0
    action: Action = field(default=Direction.STOP, compare=False)


class ReflexAgent(Agent):
    def __init__(
        self, index: int = 0, depth: int = 3, utility: UtilityFn = utility_fn
    ) -> None:
        super().__init__(index=index)
        self.depth = depth
        self.utility = utility

    def register_state(self, game_state: GameState) -> None:
        walls = game_state.get_walls()
        maze_dists = get_maze_dists(*walls.get_adjmatrix())

        if "maze_dists" in get_arg_names(self.utility):
            self.utility = partial(self.utility, maze_dists=maze_dists)

    def _get_next_states(self, state: ReflexState) -> StateGenerator:
        num_agents = state.game_state.get_num_agents()

        depth = state.depth + (1 if state.agent == num_agents - 1 else 0)
        agent = (state.agent + 1) % num_agents

        for action in state.game_state.get_legal_actions(state.agent):
            if action != Direction.STOP:
                game_state = state.game_state.generate_next(
                    state.agent, action
                )
                next_state = ReflexState(game_state, agent, depth)
                yield next_state

    def _is_terminate(self, state: ReflexState) -> bool:
        return (
            True
            if state.depth == self.depth
            or state.game_state.is_win()
            or state.game_state.is_lose()
            else False
        )


class MinimaxAgent(ReflexAgent):
    def get_action(self, game_state: GameState) -> Action:
        value = self.__alpha_beta(
            ReflexState(game_state, agent=self.index),
            alpha=-INF_COST,
            beta=INF_COST,
        )
        return value.action

    def __alpha_beta(
        self, state: ReflexState, alpha: Cost, beta: Cost
    ) -> Value:
        if self._is_terminate(state):
            return Value(self.utility(state))
        if state.agent == 0:
            return self.__max_value(state, alpha, beta)
        return self.__min_value(state, alpha, beta)

    def __max_value(
        self, state: ReflexState, alpha: Cost, beta: Cost
    ) -> Value:
        value = Value(-INF_COST)
        for next in self._get_next_states(state):
            value = max(
                value,
                Value(self.__alpha_beta(next, alpha, beta).cost, next.action),
            )
            if value.cost >= beta:
                return value
            alpha = max(alpha, value.cost)
        return value

    def __min_value(
        self, state: ReflexState, alpha: Cost, beta: Cost
    ) -> Value:
        value = Value(INF_COST)
        for next in self._get_next_states(state):
            value = min(
                value,
                Value(self.__alpha_beta(next, alpha, beta).cost, next.action),
            )
            if value.cost <= alpha:
                return value
            beta = min(beta, value.cost)
        return value

    def get_algo(self) -> Optional[str]:
        return "minimax with alpha-beta pruning"


class ExpectimaxAgent(ReflexAgent):
    def get_action(self, game_state) -> Action:
        value = self.__expectimax(ReflexState(game_state, agent=self.index))
        return value.action

    def __expectimax(self, state: ReflexState) -> Value:
        if self._is_terminate(state):
            return Value(self.utility(state))
        if state.agent == 0:
            return self.__max_value(state)
        return self.__expectation(state)

    def __max_value(self, state: ReflexState) -> Value:
        value = Value(-INF_COST)
        for next_state in self._get_next_states(state):
            value = max(
                value,
                Value(self.__expectimax(next_state).cost, next_state.action),
            )
        return value

    def __expectation(self, state: ReflexState) -> Value:
        next_states = list(self._get_next_states(state))
        value = Value()

        for next_state in next_states:
            value.cost += self.__expectimax(next_state).cost

        value.cost /= len(next_states)
        return value

    def get_algo(self) -> Optional[str]:
        return "expectimax"

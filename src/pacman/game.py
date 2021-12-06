import copy
from typing import Optional
from dataclasses import InitVar, dataclass

from .agent import Agent, AgentState, Configuration
from ..consts.direction import Direction
from ..consts.types import Action, GameResult
from ..utils.vector import Vector
from ..utils.layout import Layout
from ..utils.logger import Logger
from ..utils.timer import Timer


@dataclass
class GameStateData:
    state: InitVar["GameStateData"] = None
    _food_eaten: Vector = None
    _capsule_eaten: Vector = None
    _agent_moved: int = None
    _last_action: Action = None
    _lose: bool = False
    _win: bool = False
    score_change: int = 0

    def __post_init__(self, state: Optional["GameStateData"] = None) -> None:
        if state is not None:
            self.food = copy.deepcopy(state.food)
            self.capsules = state.capsules[:]
            self.agent_states = copy.deepcopy(state.agent_states)
            self.layout = state.layout
            self._eaten = state._eaten
            self.score = state.score

    def initialize(self, layout: Layout, num_ghost_agents: int) -> None:
        self.food = copy.deepcopy(layout.food)
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.score_change = 0

        self.agent_states = []
        num_ghosts = 0
        for is_pacman, position in layout.agent_positions:
            if not is_pacman:
                if num_ghosts == num_ghost_agents:
                    continue
                else:
                    num_ghosts += 1
            self.agent_states.append(
                AgentState(Configuration(position, Direction.STOP), is_pacman)
            )
        self._eaten = [False] * len(self.agent_states)


class Game:
    def __init__(
        self, agents: list[Agent], display, rules, log_path: str
    ) -> None:
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.game_over = False
        self.logger = Logger(log_path)
        self.timer = Timer()
        self.history = []

    def __get_result(self) -> Optional[GameResult]:
        if self.game_over:
            result = {
                "is_win": self.state.is_win(),
                "time": self.timer.elapsed,
                "score": self.state.get_score(),
                "algo": self.agents[0].get_algo(),
            }
            return result
        return None

    def run(self) -> None:
        self.display.init(self.state.data)
        self.num_moves = 0

        self.timer.start()
        for agent in self.agents:
            if hasattr(agent, "register_state"):
                agent.register_state(self.state)

        agent_idx = 0
        num_agents = len(self.agents)

        while self.game_over is False:
            agent = self.agents[agent_idx]
            action = agent.get_action(copy.deepcopy(self.state))

            self.history.append((agent_idx, action))
            self.state = self.state.generate_next(agent_idx, action)

            self.display.update(self.state.data)
            self.rules.process(self.state, self)

            if agent_idx == num_agents + 1:
                self.num_moves += 1
            agent_idx = (agent_idx + 1) % num_agents

        for agent in self.agents:
            if hasattr(agent, "final"):
                agent.final(self.state)

        self.timer.stop()
        self.display.finish()

        result = self.__get_result()
        if result is not None:
            self.logger.log_result(result)

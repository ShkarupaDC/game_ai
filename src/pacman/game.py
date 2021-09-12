import copy
from typing import Optional
from dataclasses import InitVar, dataclass

# from .search import GhostSearchProblem
from .agent import Agent, AgentState, Configuration
from ..consts.direction import Direction
from ..utils.vector import Vector
from ..utils.layout import Layout


@dataclass
class GameStateData:
    state: InitVar["GameStateData"] = None
    _food_eaten: Vector = None
    _capsule_eaten: Vector = None
    _agent_moved: int = None
    _lose: bool = False
    _win: bool = False
    score_change: int = 0

    def __post_init__(self, state: Optional["GameStateData"] = None) -> None:
        if state is not None:
            self.ghost_search = copy.deepcopy(state.ghost_search)
            self.food = copy.deepcopy(state.food)
            self.capsules = state.capsules[:]
            self.agent_states = copy.deepcopy(state.agent_states)
            self.layout = state.layout
            self._eaten = state._eaten
            self.score = state.score

    def initialize(
        self, layout: Layout, ghost_search, num_ghost_agents: int
    ) -> None:
        self.ghost_search = ghost_search
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
    def __init__(self, agents: list[Agent], display, rules) -> None:
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.game_over = False
        self.history = []

    def run(self) -> None:
        self.display.init(self.state.data)
        self.num_moves = 0

        for agent in self.agents:
            if hasattr(agent, "register"):
                agent.register(self.state)

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

        self.display.finish()

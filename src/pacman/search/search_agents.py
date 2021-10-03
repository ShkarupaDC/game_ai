from functools import partial
import inspect
from typing import Callable, Optional, Type

from .search import SearchProblem, FourPointProblem, AllFoodProblem
from .heuristics import four_point_heuristic, all_food_heuristic
from .search_solvers import a_star
from ..agent import Agent
from ...consts.direction import Direction


class SearchAgent(Agent):
    def __init__(
        self,
        search_fn: Callable,
        problem_type: Type[SearchProblem],
        heuristic: Optional[Callable] = None,
    ) -> None:
        arg_names = inspect.getargs(heuristic)[0]
        if "heuristic" in arg_names:
            self.search_fn = partial(search_fn, heuristic=heuristic)
        else:
            self.search_fn = search_fn
        self.problem_type = problem_type

    def get_action(self, game_state) -> int:
        if self.action_idx >= len(self.actions):
            return Direction.STOP
        idx = self.action_idx
        self.action_idx += 1
        return self.actions[idx]

    def register_state(self, game_state) -> None:
        problem = self.problem_type(game_state)
        self.action_idx = 0
        self.actions = self.search_fn(problem)


class FourPointAgent(SearchAgent):
    def __init__(self) -> None:
        self.search_fn = partial(a_star, heuristic=four_point_heuristic)
        self.problem_type = FourPointProblem


class AllFoodAgent(SearchAgent):
    def __init__(self) -> None:
        self.search_fn = partial(a_star, heuristic=all_food_heuristic)
        self.problem_type = AllFoodProblem

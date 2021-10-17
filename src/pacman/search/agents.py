from functools import partial
from typing import Callable, Optional, Type, Any

from .problems import SearchProblem, FourPointProblem, AllFoodProblem
from .heuristics import four_point_heuristic, all_food_heuristic
from .solvers import a_star
from ..agent import Agent
from ...consts.direction import Direction
from ...utils.general import get_arg_names


class SearchAgent(Agent):
    def __init__(
        self,
        search_fn: Callable,
        problem_type: Type[SearchProblem],
        heuristic: Optional[Callable] = None,
        **problem_kwargs: Any,
    ) -> None:
        arg_names = get_arg_names(heuristic)
        self.search_fn = (
            partial(search_fn, heuristic=heuristic)
            if "heuristic" in arg_names
            else search_fn
        )
        self.problem_type = problem_type
        self.problem_kwargs = problem_kwargs

    def get_action(self, game_state) -> int:
        if self.action_idx >= len(self.actions):
            return Direction.STOP
        idx = self.action_idx
        self.action_idx += 1
        return self.actions[idx]

    def register_state(self, game_state) -> None:
        problem = self.problem_type(
            game_state,
            **(self.problem_kwargs if hasattr(self, "problem_kwargs") else {}),
        )
        self.action_idx = 0
        self.actions = self.search_fn(problem)

    def get_algo(self) -> Optional[str]:
        algo = self.search_fn
        return (algo.func if hasattr(algo, "func") else algo).__name__


class FourPointAgent(SearchAgent):
    def __init__(self) -> None:
        self.search_fn = partial(a_star, heuristic=four_point_heuristic)
        self.problem_type = FourPointProblem


class AllFoodAgent(SearchAgent):
    def __init__(self) -> None:
        self.search_fn = partial(a_star, heuristic=all_food_heuristic)
        self.problem_type = AllFoodProblem

from typing import Any
from dataclasses import dataclass, InitVar

from .states import SearchState
from ...consts.types import Cost


@dataclass(eq=False)
class CostFn:
    game_state: InitVar[Any]

    def get_min_cost(self) -> Cost:
        raise NotImplementedError

    def __call__(self, state: SearchState) -> Cost:
        raise NotImplementedError


@dataclass(eq=False)
class UniformCostFn(CostFn):
    cost: Cost = 1

    def get_min_cost(self) -> Cost:
        return self.cost

    def __call__(self, state: SearchState) -> Cost:
        return self.cost


@dataclass(eq=False)
class FoodCostFn(CostFn):
    empty_cost: Cost = 2
    food_cost: Cost = 1

    def __post_init__(self, game_state: Any) -> None:
        self.food = game_state.get_food()

    def get_min_cost(self) -> Cost:
        return min(self.food_cost, self.empty_cost)

    def __call__(self, state: SearchState) -> Cost:
        xx, yy = state.position
        return self.food_cost if self.food[xx][yy] else self.empty_cost

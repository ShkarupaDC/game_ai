import numpy as np
from collections import defaultdict
from typing import Optional, Type

from .states import SearchState, FourPointState, AllFoodState
from .cost_fns import CostFn, UniformCostFn
from ..agent import Actions
from ...consts.direction import Direction
from ...consts.types import AdjList, Position, Cost, Action
from ...utils.data_structures import Queue, IndexMap
from ...utils.general import get_empty_adj_matrix

Neighbor = tuple[SearchState, Action, Cost]


class SearchProblem:
    def __init__(
        self,
        game_state,
        cost_fn: Type[CostFn] = UniformCostFn,
    ) -> None:
        self.history = {}
        self.walls = game_state.get_walls()
        self.cost_fn = cost_fn(game_state)

    def get_neighbor(
        self, state: SearchState, position: Position, action: Action
    ) -> Neighbor:
        raise NotImplementedError

    def get_neighbors(self, state: SearchState) -> list[Neighbor]:
        neighbors = []
        for action in Direction.as_list():
            shift = Actions.direction_to_vector(action)

            new_position = (state.position + shift).as_int()
            xx, yy = new_position

            if not self.walls[xx][yy]:
                neighbor = self.get_neighbor(state, new_position, action)
                neighbors.append(neighbor)

        return neighbors

    def is_goal(self, state: SearchState) -> bool:
        raise NotImplementedError

    def as_adj_list(self) -> tuple[AdjList, dict[Position, int]]:
        start = self.get_start()
        visited, queue = set(), Queue()
        queue.push(start)
        adj_list = defaultdict(list)
        mapping = IndexMap()

        while not queue.is_empty():
            parent = queue.pop()
            p_idx = mapping[parent.position]
            visited.add(p_idx)
            for state, _, cost in self.get_neighbors(parent):
                n_idx = mapping[state.position]
                adj_list[p_idx].append((n_idx, cost))
                if n_idx not in visited:
                    queue.push(state)

        return adj_list, mapping.as_dict()

    def get_start(self) -> Position:
        raise NotImplementedError

    def as_adj_matrix(self) -> tuple[np.ndarray, dict[Position, int]]:
        adj_list, mapping = self.as_adj_list()

        adj_matrix = get_empty_adj_matrix(len(adj_list))
        for p_idx, n_idxs in adj_list.items():
            for n_idx, cost in n_idxs:
                adj_matrix[p_idx, n_idx] = cost

        return adj_matrix, mapping

    def get_min_cost(self) -> Cost:
        return self.cost_fn.get_min_cost()


class FourPointProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        points: Optional[list[Position]] = None,
        cost_fn: Type[CostFn] = UniformCostFn,
    ) -> None:
        super().__init__(game_state, cost_fn)
        self.start = FourPointState(
            game_state.get_pacman_position(),
        )
        if points is None:
            self.points = game_state.get_food_sources()
        else:
            self.points = points
        assert len(self.points) == 4, "Invalid number of food sources"

    def get_start(self) -> FourPointState:
        return self.start

    def is_goal(self, state: FourPointState) -> bool:
        return state.bit_mask == 0b1111

    def get_neighbor(
        self, state: FourPointState, position: Position, action: Action
    ) -> Neighbor:
        if position in self.points:
            point_mask = 1 << self.points.index(position)
            bit_mask = point_mask | state.bit_mask
        else:
            bit_mask = state.bit_mask
        cost = self.cost_fn(state)

        next_state = FourPointState(position, bit_mask)
        return next_state, action, cost

    def get_points(self) -> list[Position]:
        return self.points


class AllFoodProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        cost_fn: Type[CostFn] = UniformCostFn,
    ) -> None:
        super().__init__(game_state, cost_fn)
        food = game_state.get_food_sources()
        self.start = AllFoodState(
            game_state.get_pacman_position(), frozenset(food)
        )

    def get_start(self) -> AllFoodState:
        return self.start

    def is_goal(self, state: AllFoodState) -> bool:
        return len(state.rest) == 0

    def get_neighbor(
        self, state: AllFoodState, position: Position, action: Action
    ) -> Neighbor:
        rest = (
            state.rest - set([position])
            if position in state.rest
            else state.rest
        )
        next_state = AllFoodState(position, rest)
        cost = self.cost_fn(state)
        return next_state, action, cost

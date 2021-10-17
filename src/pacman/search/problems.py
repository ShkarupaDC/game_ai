from collections import defaultdict
from typing import Optional, Type, Any

from .states import SearchState, FourPointState, AllFoodState
from .cost_fns import CostFn, UniformCostFn
from ..agent import Actions
from ...consts.direction import Direction
from ...consts.types import (
    AdjList,
    AdjMatrix,
    PosToIdx,
    Position,
    Cost,
    Action,
)
from ...utils.graph import adjlist_to_adjmatrix
from ...utils.data_structures import Queue

Neighbor = tuple[SearchState, Action, Cost]


class SearchProblem:
    def __init__(
        self,
        game_state,
        cost_fn: Type[CostFn] = UniformCostFn,
        **cost_kwargs: Any,
    ) -> None:
        self.history = {}
        self.walls = game_state.get_walls()
        self.cost_fn = cost_fn(game_state, **cost_kwargs)

    def get_neighbor(
        self, state: SearchState, position: Position, action: Action
    ) -> Neighbor:
        raise NotImplementedError

    def get_neighbors(self, state: SearchState) -> list[Neighbor]:
        neighbors = []
        for action in Direction.as_list():
            move = Actions.direction_to_vector(action)

            position = (state.position + move).as_int()
            xx, yy = position

            if not self.walls[xx][yy]:
                neighbor = self.get_neighbor(state, position, action)
                neighbors.append(neighbor)

        return neighbors

    def is_goal(self, state: SearchState) -> bool:
        raise NotImplementedError

    def get_start(self) -> Position:
        raise NotImplementedError

    def get_adjlist(self) -> AdjList:
        adjlist = defaultdict(list)
        start = self.get_start()
        visited = set()
        queue = Queue()
        queue.push(start)

        while not queue.is_empty():
            parent = queue.pop()
            visited.add(parent.position)

            for state, _, cost in self.get_neighbors(parent):
                if state.position not in visited:
                    queue.push(state)
                adjlist[parent.position].append((state.position, cost))

        return adjlist

    def get_adjmatrix(self) -> tuple[AdjMatrix, PosToIdx]:
        adjlist = self.get_adjlist()
        return adjlist_to_adjmatrix(adjlist)

    def get_min_cost(self) -> Cost:
        return self.cost_fn.get_min_cost()


class PositionProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        goal: Position,
        start: Optional[Position] = None,
        cost_fn: Type[CostFn] = UniformCostFn,
        **cost_kwargs: Any,
    ) -> None:
        super().__init__(game_state, cost_fn, **cost_kwargs)
        self.start = SearchState(
            start if start is not None else game_state.get_pacman_position()
        )
        self.goal = goal

    def is_goal(self, state: SearchState) -> bool:
        return state.position == self.goal

    def get_start(self) -> Position:
        return self.start

    def get_neighbor(
        self, state: SearchState, position: Position, action: Action
    ) -> Neighbor:
        next_state = SearchState(position)
        cost = self.cost_fn(next_state)
        return next_state, action, cost

    def get_goal(self) -> Position:
        return self.goal


class FourPointProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        points: Optional[list[Position]] = None,
        cost_fn: Type[CostFn] = UniformCostFn,
        **cost_kwargs: Any,
    ) -> None:
        super().__init__(game_state, cost_fn, **cost_kwargs)
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
        next_state = FourPointState(position, bit_mask)

        cost = self.cost_fn(next_state)
        return next_state, action, cost

    def get_points(self) -> list[Position]:
        return self.points


class AllFoodProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        cost_fn: Type[CostFn] = UniformCostFn,
        **cost_kwargs: Any,
    ) -> None:
        super().__init__(game_state, cost_fn, **cost_kwargs)
        self.food = game_state.get_food_sources()
        self.start = AllFoodState(
            game_state.get_pacman_position(), frozenset(self.food)
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
        cost = self.cost_fn(next_state)
        return next_state, action, cost

    def get_food(self) -> list[Position]:
        return self.food

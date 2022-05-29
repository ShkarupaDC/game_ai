import itertools

from .states import FourPointState, AllFoodState, SearchState
from .problems import FourPointProblem, AllFoodProblem, PositionProblem
from ...utils.graph import get_maze_dists


def distance_heuristic(
    state: SearchState,
    problem: PositionProblem,
    metric: str = "manhattan",
) -> float:
    if problem.is_goal(state):
        return 0
    goal = problem.get_goal()
    metric = getattr(state.position, metric)
    return problem.get_min_cost() * metric(goal)


def four_point_heuristic(
    state: FourPointState, problem: FourPointProblem
) -> float:
    if problem.is_goal(state):
        return 0
    rest_points = [
        point
        for idx, point in enumerate(problem.get_points())
        if 1 << idx & state.bit_mask == 0b0000
    ]
    paths = itertools.permutations(rest_points)
    distances = [
        sum(
            problem.get_min_cost() * xx.manhattan(yy)
            for xx, yy in zip([state.position, *path[:-1]], path)
        )
        for path in paths
    ]
    min_distance = min(distances)
    return min_distance


def all_food_heuristic(state: AllFoodState, problem: AllFoodProblem) -> float:
    if problem.is_goal(state):
        return 0
    memory = problem.history.get("memory")
    if memory is None:
        memory = get_maze_dists(
            *problem.get_adjmatrix(), goals=problem.get_food()
        )
        problem.history["memory"] = memory
    path_lens = [
        problem.get_min_cost() * memory.get(state.position, goal)
        for goal in list(state.rest)
    ]
    return min(path_lens)


def suboptimal_all_food_heuristic(
    state: AllFoodState, problem: AllFoodProblem, metric: str = "manhattan"
) -> float:
    if problem.is_goal(state):
        return 0
    metric = getattr(state.position, metric)
    distances = [
        problem.get_min_cost() * metric(goal) for goal in list(state.rest)
    ]
    return min(distances)

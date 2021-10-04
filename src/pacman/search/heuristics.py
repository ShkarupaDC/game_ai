from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
import itertools

from .states import FourPointState, AllFoodState, SearchState
from .search import FourPointProblem, AllFoodProblem, PositionPoblem
from ...consts.game import HEURISTIC_SCALER
from ...utils.data_structures import DistanceMemory


def distance_heuristic(
    state: SearchState,
    problem: PositionPoblem,
    metric: str = "manhattan",
    greedy: bool = False,
) -> float:
    if problem.is_goal(state):
        return 0
    scaler = HEURISTIC_SCALER if greedy else 1
    goal = problem.get_goal()
    metric = getattr(state.position, metric)
    return scaler * problem.get_min_cost() * metric(goal)


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
        adj_matrix, mapping = problem.as_adj_matrix()
        adj_matrix = csr_matrix(adj_matrix)
        goal_idxs = {
            mapping[goal]: idx for idx, goal in enumerate(problem.get_food())
        }
        dist = shortest_path(
            adj_matrix,
            directed=False,
            return_predecessors=False,
            indices=list(goal_idxs.keys()),
        )
        memory = DistanceMemory(dist, mapping, goal_idxs)
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

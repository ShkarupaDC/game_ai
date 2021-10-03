import random
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
import itertools

from .states import FourPointState, AllFoodState
from .search import FourPointProblem, AllFoodProblem
from ...utils.data_structures import DistanceMemory


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
    rest_goals = list(state.rest)

    if memory is None:
        adj_matrix, mapping = problem.as_adj_matrix()
        adj_matrix = csr_matrix(adj_matrix)

        dist = shortest_path(adj_matrix, "auto", False, False)
        memory = DistanceMemory(dist, mapping)
        problem.history["memory"] = memory

    path_lens = [
        problem.get_min_cost() * memory.get(state.position, goal)
        for goal in rest_goals
    ]
    return min(path_lens)

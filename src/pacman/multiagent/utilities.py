import random

from .states import ReflexState
from ...consts.types import Cost
from ...consts.game import INF_COST
from ...utils.data_structures import MazeDistance

EPS = 1e-3


def utility_fn(
    state: ReflexState, maze_dists: MazeDistance, dist_mult=1e2, food_mult=1e4
) -> Cost:
    game_state = state.game_state

    pacman = game_state.get_pacman_position()
    food_dists = [
        maze_dists.get(pacman, food) for food in game_state.get_food_sources()
    ]
    food_dist = clip(food_dists) if food_dists else EPS
    ghost_dists = [
        maze_dists.get(pacman, ghost)
        for ghost in game_state.get_ghost_positions()
    ]
    ghost_dist = clip(ghost_dists) if ghost_dists else INF_COST
    num_food = game_state.get_num_food()

    game_score = (
        dist_mult / (food_dist if food_dist < 2 * ghost_dist else -ghost_dist)
        + food_mult / num_food
        + random.randint(-2, 2)
    )
    return game_score


def clip(values: list[Cost], eps: float = EPS):
    return max(min(values), eps)

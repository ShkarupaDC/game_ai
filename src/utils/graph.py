import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
from typing import Optional

from .data_structures import MazeDistance
from ..consts.types import AdjList, AdjMatrix, PosToIdx, Position


def adjlist_to_adjmatrix(adjlist: AdjList) -> tuple[AdjMatrix, PosToIdx]:
    mapping = {position: idx for idx, position in enumerate(adjlist)}
    num_nodes = len(mapping)
    adjmatrix = get_empty_adjmatrix(num_nodes)

    for parent, neighbors in adjlist.items():
        p_idx = mapping[parent]
        for neighbor, cost in neighbors:
            n_idx = mapping[neighbor]
            adjmatrix[p_idx, n_idx] = cost

    return adjmatrix, mapping


def get_empty_adjmatrix(size: int) -> np.ndarray:
    adjmatrix = np.full((size, size), float("inf"))
    np.fill_diagonal(adjmatrix, 0)
    return adjmatrix


def get_maze_dists(
    adjmatrix: AdjMatrix,
    mapping: PosToIdx,
    goals: Optional[list[Position]] = None,
) -> MazeDistance:
    sparse_matrix = csr_matrix(adjmatrix)
    if goals is not None:
        goal_mapping = {mapping[goal]: idx for idx, goal in enumerate(goals)}
        goal_idxs = list(goal_mapping.keys())
    else:
        goal_mapping = goal_idxs = None
    maze_dists = shortest_path(
        sparse_matrix,
        directed=False,
        return_predecessors=False,
        indices=goal_idxs,
    )
    return MazeDistance(maze_dists, mapping, goal_mapping)

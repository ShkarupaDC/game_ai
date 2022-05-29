from typing import Callable

from .problems import SearchProblem
from ...consts.game import INF_COST
from ...consts.types import Action
from ...utils.data_structures import Stack, Queue, PriorityQueue
from ...utils.timer import time_it


@time_it()
def bfs(problem: SearchProblem) -> list[Action]:
    # For cost = const
    start = problem.get_start()
    visited = set()
    queue = Queue()
    queue.push((start, []))

    while not queue.is_empty():
        parent, actions = queue.pop()
        visited.add(parent)
        if problem.is_goal(parent):
            return actions
        for state, action, _ in problem.get_neighbors(parent):
            if state in visited:
                continue
            new_actions = actions + [action]
            queue.push((state, new_actions))

    return []


@time_it()
def dfs(problem: SearchProblem) -> list[Action]:
    # Not optimal path
    start = problem.get_start()
    visited = set()
    stack = Stack()
    stack.push(start)

    while not stack.is_empty():
        parent, actions = stack.pop()
        visited.add(parent)
        if problem.is_goal(parent):
            return actions
        for state, action, _ in problem.get_neighbors(parent):
            if state in visited:
                continue
            new_actions = actions + [action]
            stack.push((state, new_actions))

    return []


@time_it(True)
def ucs(problem: SearchProblem) -> list[list[Action]]:
    start = problem.get_start()
    costs = {start: 0}
    visited = set()
    queue = PriorityQueue()
    queue.push((start, []), 0)

    while not queue.is_empty():
        (parent, actions), cost = queue.pop()
        visited.add(parent)
        if costs[parent] < cost:
            continue
        if problem.is_goal(parent):
            return actions
        for state, action, move_cost in problem.get_neighbors(parent):
            if state in visited:
                continue
            new_cost = cost + move_cost
            if new_cost < costs.get(state, INF_COST):
                new_actions = actions + [action]
                costs[state] = new_cost
                queue.push((state, new_actions), new_cost)

    return []


@time_it()
def a_star(
    problem: SearchProblem, heuristic: Callable, greedy: bool = False
) -> list[Action]:
    start = problem.get_start()
    costs = {start: 0}
    visited = set()
    queue = PriorityQueue()
    queue.push((start, []), 0)

    while not queue.is_empty():
        (parent, actions), _ = queue.pop()
        visited.add(parent)
        cost = costs[parent]
        if problem.is_goal(parent):
            return actions
        for state, action, move_cost in problem.get_neighbors(parent):
            if state in visited:
                continue
            new_cost = cost + move_cost
            if new_cost < costs.get(state, INF_COST):
                new_actions = actions + [action]
                priority = heuristic(state, problem)
                if not greedy:
                    priority += new_cost
                costs[state] = new_cost
                queue.push((state, new_actions), priority)

    return []

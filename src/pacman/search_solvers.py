from ..consts.game import INF_COST
from ..consts.types import Action
from ..utils.data_structures import Stack, Queue, PriorityQueue
from ..utils.search import find_path
from ..utils.general import bitwise_or, time_it


@time_it()
def bfs(problem) -> list[list[Action]]:
    # For cost = const
    start = problem.get_start()
    goals = problem.get_goals()

    found = [False] * len(goals)
    visited = set()
    memory = dict()
    queue = Queue()
    queue.push((start, 0))

    while not queue.is_empty():
        parent, cost = queue.pop()
        visited.add(parent)

        found = bitwise_or(found, problem.in_goals(parent))
        if all(found) is True:
            break
        for node, move_cost in problem.get_neighbors(parent):
            if node in visited:
                continue
            new_cost = cost + move_cost
            memory[node] = parent
            queue.push((node, new_cost))

    return [find_path(start, goal, memory) for goal in goals]


@time_it()
def dfs(problem) -> list[list[Action]]:
    start = problem.get_start()
    goals = problem.get_goals()

    costs = {start: 0}
    memory = dict()
    stack = Stack()
    stack.push(start)

    while not stack.is_empty():
        parent = stack.pop()
        cost = costs[parent]

        for node, move_cost in problem.get_neighbors(parent):
            new_cost = cost + move_cost
            if costs.get(node, INF_COST) <= new_cost:
                continue
            memory[node] = parent
            stack.push(node)
            costs[node] = new_cost

    return [find_path(start, goal, memory) for goal in goals]


@time_it()
def ucs(problem) -> list[list[Action]]:
    start = problem.get_start()
    goals = problem.get_goals()

    found = [False] * len(goals)
    costs = {start: 0}
    visited = set()
    memory = dict()
    queue = PriorityQueue()
    queue.push(start, 0)

    while not queue.is_empty():
        parent, cost = queue.pop()
        visited.add(parent)
        if costs[parent] < cost:
            continue
        found = bitwise_or(found, problem.in_goals(parent))
        if all(found) is True:
            break
        for node, move_cost in problem.get_neighbors(parent):
            if node in visited:
                continue
            new_cost = cost + move_cost
            if new_cost < costs.get(node, INF_COST):
                costs[node] = new_cost
                memory[node] = parent
                queue.push(node, new_cost)

    return [find_path(start, goal, memory) for goal in goals]

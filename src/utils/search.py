from ..consts.types import Position, Action


def find_path(
    start: Position, goal: Position, memory: dict[Position, Position]
) -> list[Action]:
    path = []
    while goal in memory:
        parent = memory[goal]
        if parent == start:
            break
        goal = parent
        path.append(parent)
    path.reverse()
    return path

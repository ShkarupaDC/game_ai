from ..utils.vector import Vector


class Direction:
    WEST = -2
    SOUTH = -1
    STOP = 0
    NORTH = 1
    EAST = 2

    @staticmethod
    def as_list(with_stop: bool = False):
        directions = [
            Direction.WEST,
            Direction.SOUTH,
            Direction.NORTH,
            Direction.EAST,
        ]
        if with_stop:
            directions += [Direction.STOP]
        return directions


TO_VECTOR = {
    Direction.NORTH: Vector(0, 1),
    Direction.SOUTH: Vector(0, -1),
    Direction.EAST: Vector(1, 0),
    Direction.WEST: Vector(-1, 0),
    Direction.STOP: Vector(0, 0),
}


class MazeMove:
    LEFT = Vector(-2, 0)
    RIGTH = Vector(2, 0)
    UP = Vector(0, 2)
    DOWN = Vector(0, -2)

from ..utils.vector import Vector


class Directions:
    WEST = -2
    SOUTH = -1
    STOP = 0
    NORTH = 1
    EAST = 2


DIRECTION_TO_VECTOR = {
    Directions.NORTH: Vector(0, 1),
    Directions.SOUTH: Vector(0, -1),
    Directions.EAST: Vector(1, 0),
    Directions.WEST: Vector(-1, 0),
    Directions.STOP: Vector(0, 0),
}

from ..utils.general import color_to_vector


class Color:
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    RED = "#E50000"
    BLUE = "#004CE5"
    ORANGE = "#F96811"
    GREEN = "#19BFB2"
    GRAY = "#E5E5E5"
    DARK_GREEN = "#666600"
    LIGHT_BLUE = "#0033FF"
    LIGHT_YELLOW = "#FFFF3D"


class MainWindow:
    GRID_SIZE = 30.0
    BACKGROUND_COLOR = Color.BLACK


class Wall:
    COLOR = Color.LIGHT_BLUE


class Info:
    COLOR = Color.DARK_GREEN
    HEIGHT = 35
    SCORE_COLOR = Color.GRAY


class Ghost:
    SCARED_COLOR = Color.WHITE
    COLORS = [
        Color.RED,
        Color.BLUE,
        Color.ORANGE,
        Color.GREEN,
    ]
    VECTOR_COLORS = [color_to_vector(color) for color in COLORS]
    SHAPE = [
        (0, 0.3),
        (0.25, 0.75),
        (0.5, 0.3),
        (0.75, 0.75),
        (0.75, -0.5),
        (0.5, -0.75),
        (-0.5, -0.75),
        (-0.75, -0.5),
        (-0.75, 0.75),
        (-0.5, 0.3),
        (-0.25, 0.75),
    ]
    SIZE = 0.65


class Pacman:
    COLOR = Color.LIGHT_YELLOW
    SCALE = 0.5
    OUTLINE_WIDTH = 2
    FRAMES = 4.0


class Food:
    COLOR = Color.WHITE
    SIZE = 0.1


class Capsule:
    COLOR = Color.WHITE
    SIZE = 0.25

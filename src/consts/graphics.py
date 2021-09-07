from ..utils.general import format_color, color_to_vector


class Color:
    WHITE = format_color(1.0, 1.0, 1.0)
    BLACK = format_color(0.0, 0.0, 0.0)
    RED = format_color(0.9, 0.0, 0.0)
    BLUE = format_color(0.0, 0.3, 0.9)
    ORANGE = format_color(0.98, 0.41, 0.07)
    GREEN = format_color(0.1, 0.75, 0.7)
    GRAY = format_color(0.9, 0.9, 0.9)
    DARK_GREEN = format_color(0.4, 0.4, 0)
    LIGHT_BLUE = format_color(0.0, 0.2, 1.0)
    LIGHT_YELLOW = format_color(1.0, 1.0, 0.24)


DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = Color.BLACK
WALL_COLOR = Color.LIGHT_BLUE
INFO_PANE_COLOR = Color.DARK_GREEN
SCORE_COLOR = Color.GRAY

GHOST_COLORS = [
    Color.RED,
    Color.BLUE,
    Color.ORANGE,
    Color.GREEN,
]
GHOST_SIZE = 0.65
SCARED_COLOR = Color.WHITE
GHOST_VEC_COLORS = [color_to_vector(color) for color in GHOST_COLORS]
GHOST_SHAPE = [
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
PACMAN_COLOR = Color.LIGHT_YELLOW
PACMAN_SCALE = 0.5
PACMAN_OUTLINE_WIDTH = 2

FOOD_COLOR = Color.WHITE
FOOD_SIZE = 0.1
CAPSULE_COLOR = Color.WHITE
CAPSULE_SIZE = 0.25

FRAMES = 4.0

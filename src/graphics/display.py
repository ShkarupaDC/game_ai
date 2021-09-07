import math
from tkinter import Grid
from typing import Optional, Union

from ..consts.graphics import *
from ..consts.direction import Directions
from ..utils.layout import Layout
from ..utils.vector import Vector
from ..graphics.ui import UI
from ..pacman.rules import GameState
from ..pacman.game import AgentState


class InfoPane:
    def __init__(self, ui: UI, layout: Layout, grid_size: int):
        self.ui = ui
        self.grid_size = grid_size
        self.base = (layout.height + 1) * grid_size
        self.font_size = 24
        self.text_color = PACMAN_COLOR
        self.draw_pane()

    def to_screen(self, position: tuple[float, float]) -> tuple[float, float]:
        shift = Vector(self.grid_size, self.base)
        position = Vector(*position)
        return (shift + position).as_tuple()

    def draw_pane(self) -> None:
        self.score_text = self.ui.text(
            self.to_screen((0, 0)),
            self.text_color,
            "SCORE:    0",
            "Times",
            self.font_size,
            "bold",
        )

    def update_score(self, score: int) -> None:
        self.ui.change_text(self.score_text, "SCORE: % 4d" % score)


class PacmanGraphics:
    def __init__(
        self,
        ui: UI,
        zoom: float = 1.0,
        frame_time: float = 0.0,
    ) -> None:
        self.ui = ui
        self.have_window = 0
        self.zoom = zoom
        self.grid_size = DEFAULT_GRID_SIZE * zoom
        self.frame_time = frame_time

    def init(self, state: GameState) -> None:
        self.__start_graphics(state)
        self.__draw_static_objects()
        self.__draw_agents(state)

    def __start_graphics(self, state: GameState) -> None:
        self.layout = state.layout
        self.width = self.layout.width
        self.height = self.layout.height
        self.__make_window(self.width, self.height)
        self.info_pane = InfoPane(self.ui, self.layout, self.grid_size)

    def __draw_static_objects(self) -> None:
        layout = self.layout
        self.__draw_walls(layout.walls)
        self.food = self.__draw_food(layout.food)
        self.capsules = self.__draw_capsules(layout.capsules)
        self.ui.refresh()

    def __draw_agents(self, state: GameState) -> None:
        self.agent_images = [
            (
                agent,
                self.__draw_pacman(agent)
                if agent.is_pacman
                else self.__draw_ghost(agent, idx),
            )
            for idx, agent in enumerate(state.agent_states)
        ]
        self.ui.refresh()

    def __swap_images(self, agent_idx: int, new_state: AgentState) -> None:
        prev_image = self.agent_images[agent_idx][1]
        for image in prev_image:
            self.ui.remove_from_screen(image)

        image = (
            self.__draw_pacman(new_state)
            if new_state.is_pacman
            else self.__draw_ghost(new_state, agent_idx)
        )
        self.agent_images[agent_idx] = (new_state, image)
        self.ui.refresh()

    def update(self, new_state: GameState) -> None:
        agent_idx = new_state._agent_moved
        state = new_state.agent_states[agent_idx]

        if self.agent_images[agent_idx][0].is_pacman != state.is_pacman:
            self.__swap_images(agent_idx, state)
        prev_state, prev_image = self.agent_images[agent_idx]

        if state.is_pacman:
            self.__animate_pacman(state, prev_state, prev_image)
        else:
            self.__move_ghost(state, agent_idx, prev_image)
        self.agent_images[agent_idx] = (state, prev_image)

        if new_state._capsule_eaten is not None:
            self.__remove_capsules(new_state._capsule_eaten, self.capsules)
        if new_state._food_eaten is not None:
            self.__remove_food(new_state._food_eaten, self.food)

        self.info_pane.update_score(new_state.score)

    def __make_window(self, width: int, height: int) -> None:
        offset = 2 * self.grid_size

        grid_height = self.grid_size * (height - 1)
        grid_width = self.grid_size * (width - 1)

        self.ui.init_ui(
            grid_width + offset,
            grid_height + offset + INFO_PANE_HEIGHT,
            color=BACKGROUND_COLOR,
            title="Pacman",
        )

    def __draw_pacman(self, pacman: AgentState) -> list[int]:
        body = self.ui.circle(
            self.to_screen(self.__get_position(pacman)),
            PACMAN_SCALE * self.grid_size,
            PACMAN_COLOR,
            PACMAN_COLOR,
            self.get_endpoints(self.__get_direction(pacman)),
            width=PACMAN_OUTLINE_WIDTH,
        )
        return [body]

    def get_endpoints(
        self, direction: int, position: Vector = Vector()
    ) -> tuple[float, float]:
        shift = position.manhattan(position.as_int())

        width = 30 + 80 * math.sin(math.pi * shift)
        delta = width / 2

        endpoints = {
            Directions.WEST: (180 + delta, 180 - delta),
            Directions.NORTH: (90 + delta, 90 - delta),
            Directions.STOP: (delta, -delta),
            Directions.SOUTH: (270 + delta, 270 - delta),
            Directions.EAST: (delta, -delta),
        }
        return endpoints[direction]

    def move_pacman(
        self, position: Vector, direction: int, image: list[int]
    ) -> None:
        screen = self.to_screen(position)
        endpoints = self.get_endpoints(direction, position)

        radius = PACMAN_SCALE * self.grid_size

        self.ui.move_circle(image[0], screen, radius, endpoints)
        self.ui.refresh()

    def __animate_pacman(
        self, pacman: AgentState, prev_pacman: AgentState, image: int
    ) -> None:
        if self.frame_time > 0.01 or self.frame_time < 0:
            x, y = self.__get_position(pacman)
            xx, yy = self.__get_position(prev_pacman)

            for idx in range(1, int(FRAMES) + 1):
                position = Vector(
                    x * idx / FRAMES + xx * (FRAMES - idx) / FRAMES,
                    y * idx / FRAMES + yy * (FRAMES - idx) / FRAMES,
                )
                self.move_pacman(
                    position,
                    self.__get_direction(pacman),
                    image,
                )
                self.ui.refresh()
                self.ui.sleep(abs(self.frame_time) / FRAMES)
        else:
            self.move_pacman(
                self.__get_position(pacman),
                self.__get_direction(pacman),
                image,
            )
        self.ui.refresh()

    def __get_ghost_color(self, ghost: AgentState, ghost_idx: int) -> int:
        if ghost.scared_timer > 0:
            return SCARED_COLOR
        else:
            return GHOST_COLORS[ghost_idx]

    def __draw_ghost(self, ghost, agent_idx: int) -> list[int]:
        screen_x, screen_y = self.to_screen(self.__get_position(ghost))
        coords = [
            (
                x * self.grid_size * GHOST_SIZE + screen_x,
                y * self.grid_size * GHOST_SIZE + screen_y,
            )
            for x, y in GHOST_SHAPE
        ]
        colour = self.__get_ghost_color(ghost, agent_idx)
        body = self.ui.polygon(coords, colour, filled=1)
        return [body]

    def __move_ghost(
        self, ghost: AgentState, ghost_idx: int, image_parts: list[int]
    ) -> None:
        new_x, new_y = self.to_screen(self.__get_position(ghost))

        for image_part in image_parts:
            self.ui.move_to(image_part, new_x, new_y)
        self.ui.refresh()

        color = self.__get_ghost_color(ghost, ghost_idx)
        self.ui.edit(image_parts[0], fill=color, outline=color)
        self.ui.refresh()

    def __get_position(self, agent_state: AgentState) -> Vector:
        if agent_state.configuration is None:
            return Vector(-1e3, -1e3)
        return agent_state.get_position()

    def __get_direction(self, agent_state: AgentState) -> int:
        if agent_state.configuration is None:
            return Directions.STOP
        return agent_state.get_direction()

    def finish(self) -> None:
        self.ui.end_graphics()

    def to_screen(
        self, point: Union[Vector, tuple[float, float]]
    ) -> tuple[float, float]:
        x, y = point
        x = (x + 1) * self.grid_size
        y = (self.height - y) * self.grid_size
        return x, y

    def __draw_walls(self, walls: Grid) -> None:
        for x, row in enumerate(walls):
            for y, cell in enumerate(row):
                if cell:
                    screen = Vector(*self.to_screen((x, y)))

                    west_is_wall = self.__is_wall(x - 1, y, walls)
                    east_is_wall = self.__is_wall(x + 1, y, walls)
                    north_is_wall = self.__is_wall(x, y + 1, walls)
                    south_is_wall = self.__is_wall(x, y - 1, walls)

                    if (
                        (south_is_wall and north_is_wall)
                        or (south_is_wall and north_is_wall)
                        or (west_is_wall and south_is_wall)
                        or south_is_wall
                    ):
                        end_shift = Vector(0, self.grid_size)
                        self.ui.line(
                            screen.as_tuple(),
                            (screen + end_shift).as_tuple(),
                            WALL_COLOR,
                        )
                    if (
                        (east_is_wall and west_is_wall)
                        or (south_is_wall and east_is_wall)
                        or (east_is_wall and north_is_wall)
                        or east_is_wall
                    ):
                        end_shift = Vector(self.grid_size, 0)
                        self.ui.line(
                            screen.as_tuple(),
                            (screen + end_shift).as_tuple(),
                            WALL_COLOR,
                        )

    def __is_wall(self, x: int, y: int, walls: Grid) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def __draw_food(self, food: Grid) -> list[list[Optional[int]]]:
        food_images = []
        for x, row in enumerate(food):
            image_row = []
            food_images.append(image_row)
            for y, cell in enumerate(row):
                if cell:
                    screen = self.to_screen((x, y))
                    point = self.ui.circle(
                        screen,
                        FOOD_SIZE * self.grid_size,
                        FOOD_COLOR,
                        FOOD_COLOR,
                        width=1,
                    )
                    image_row.append(point)
                else:
                    image_row.append(None)
        return food_images

    def __draw_capsules(self, capsules: list[Vector]) -> dict:
        capsule_images = {}
        for capsule in capsules:
            screen = self.to_screen(capsule)
            point = self.ui.circle(
                screen,
                CAPSULE_SIZE * self.grid_size,
                CAPSULE_COLOR,
                CAPSULE_COLOR,
                width=1,
            )
            capsule_images[capsule] = point
        return capsule_images

    def __remove_food(self, cell: Vector, food_images: list[int]) -> None:
        x, y = cell
        self.ui.remove_from_screen(food_images[x][y])

    def __remove_capsules(
        self, cell: Vector, capsuleImages: list[int]
    ) -> None:
        self.ui.remove_from_screen(capsuleImages[cell])

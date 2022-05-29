import time
import tkinter
from typing import Optional

from ..consts.graphics import Color, Key

DONT_WAIT = tkinter._tkinter.DONT_WAIT


class UI:
    master = None
    keys_down = {}
    keys_wait = {}
    got_release = None

    @staticmethod
    def init_ui(
        width: int = 640,
        height: int = 480,
        color: str = Color.BLACK,
        title: str = "Graphics Window",
    ) -> None:
        if UI.master is not None:
            UI.master.destroy()

        UI.canvas_ys = UI.canvas_y = height - 1
        UI.canvas_xs = UI.canvas_x = width - 1

        UI.master = tkinter.Tk()
        UI.master.protocol("WM_DELETE_WINDOW", exit)
        UI.master.title(title)
        UI.master.resizable(0, 0)

        UI.bg_color = color
        try:
            UI.canvas = tkinter.Canvas(UI.master, width=width, height=height)
            UI.canvas.pack()
            UI.draw_background()
            UI.canvas.update()
        except:
            raise Exception("Can not create canvas to draw on")

        UI.master.bind("<KeyPress>", UI.__key_press)
        UI.master.bind("<KeyRelease>", UI.__key_release)
        UI.__clear_keys()

    @staticmethod
    def draw_background() -> None:
        corners = [
            (0, 0),
            (0, UI.canvas_ys),
            (UI.canvas_xs, UI.canvas_ys),
            (UI.canvas_xs, 0),
        ]
        UI.polygon(
            corners,
            UI.bg_color,
            fill_color=UI.bg_color,
            filled=True,
            smoothed=False,
        )

    @staticmethod
    def refresh() -> None:
        UI.canvas.update_idletasks()

    @staticmethod
    def sleep(seconds: int) -> None:
        if UI.master is None:
            time.sleep(seconds)
        else:
            UI.master.update_idletasks()
            pause_time = int(1e3 * seconds)
            UI.master.after(pause_time, UI.master.quit)
            UI.master.mainloop()

    @staticmethod
    def end_graphics() -> None:
        try:
            UI.sleep(seconds=1)
            if UI.master is not None:
                UI.master.destroy()
        finally:
            UI.master = None
            UI.canvas = None
            UI.__clear_keys()

    @staticmethod
    def edit(id: int, **kwargs):
        UI.canvas.itemconfigure(id, **kwargs)

    def polygon(
        coords: list[tuple[float, float]],
        outline_color: str,
        fill_color: Optional[str] = None,
        filled: int = 1,
        smoothed: int = 1,
        behind: int = 0,
        width: int = 1,
    ) -> int:
        coord_list = [dim for coord in coords for dim in coord]
        if fill_color is None:
            fill_color = outline_color
        if filled == 0:
            fill_color = ""
        polygon = UI.canvas.create_polygon(
            coord_list,
            outline=outline_color,
            fill=fill_color,
            smooth=smoothed,
            width=width,
        )
        if behind > 0:
            UI.canvas.tag_lower(polygon, behind)
        return polygon

    @staticmethod
    def circle(
        position: tuple[float, float],
        radius: int,
        outline_color: str,
        fill_color: Optional[str] = None,
        endpoints: Optional[tuple[float, float]] = None,
        style: str = "pieslice",
        width: int = 2,
    ) -> int:
        x, y = position

        x1, x2 = x - radius - 1, x + radius
        y1, y2 = y - radius - 1, y + radius

        if endpoints is None:
            end_x, end_y = 0, 359
        else:
            end_x, end_y = tuple(endpoints)

        while end_x > end_y:
            end_y += 360
        return UI.canvas.create_arc(
            x1,
            y1,
            x2,
            y2,
            outline=outline_color,
            fill=fill_color or outline_color,
            extent=end_y - end_x,
            start=end_x,
            style=style,
            width=width,
        )

    @staticmethod
    def move_circle(
        id: int,
        position: tuple[float, float],
        radius: int,
        endpoints: Optional[tuple[float, float]] = None,
    ) -> None:
        x, y = position
        x1 = x - radius - 1
        y1 = y - radius - 1

        if endpoints is None:
            end_x, end_y = 0, 359
        else:
            end_x, end_y = tuple(endpoints)

        while end_x > end_y:
            end_y += 360

        UI.edit(id, start=end_x, extent=end_y - end_x)
        UI.move_to(id, x1, y1)

    @staticmethod
    def line(
        start: tuple[float, float],
        end: tuple[float, float],
        color: str = Color.BLACK,
        width: int = 2,
    ) -> int:
        return UI.canvas.create_line(*start, *end, fill=color, width=width)

    @staticmethod
    def remove_from_screen(x: int) -> None:
        UI.canvas.delete(x)
        UI.master.dooneevent(DONT_WAIT)

    @staticmethod
    def move_to(object, x: float, y: Optional[float] = None) -> None:
        new_coords = []
        current_x, current_y = UI.canvas.coords(object)[0:2]
        horizontal = True

        for coord in UI.canvas.coords(object):
            add = x - current_x if horizontal else y - current_y
            horizontal = not horizontal
            new_coords.append(coord + add)

        UI.canvas.coords(object, *new_coords)
        UI.master.dooneevent(DONT_WAIT)

    @staticmethod
    def __key_press(event: tkinter.Event) -> None:
        UI.keys_down[event.keysym] = 1
        if event.keysym in Key.control_keys():
            UI.keys_wait[event.keysym] = 1
        UI.got_release = None

    @staticmethod
    def __key_release(event: tkinter.Event) -> None:
        try:
            del UI.keys_down[event.keysym]
        except:
            pass
        UI.got_release = 1

    @staticmethod
    def __clear_keys(event: Optional[tkinter.Event] = None) -> None:
        UI.keys_down = {}
        UI.keys_wait = {}
        UI.got_release = None

    @staticmethod
    def keys_pressed() -> list[str]:
        UI.master.dooneevent(DONT_WAIT)
        if UI.got_release != 0:
            UI.master.dooneevent(DONT_WAIT)
        return list(UI.keys_down.keys())

    @staticmethod
    def keys_waiting() -> list[str]:
        keys = list(UI.keys_wait.keys())
        UI.keys_wait = {}
        return keys

    @staticmethod
    def text(
        position: tuple[float, float],
        color: str,
        contents: str,
        font: str = "Helvetica",
        size: int = 12,
        style: str = "normal",
        anchor: str = "nw",
    ) -> int:
        return UI.canvas.create_text(
            *position,
            fill=color,
            text=contents,
            font=(font, str(size), style),
            anchor=anchor
        )

    @staticmethod
    def change_text(
        id: int,
        new_text: str,
        font: Optional[str] = None,
        size: int = 12,
        style: str = "normal",
    ):
        UI.canvas.itemconfigure(id, text=new_text)
        if font is not None:
            UI.canvas.itemconfigure(id, font=(font, "-%d" % size, style))

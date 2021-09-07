import time
import tkinter
from typing import Optional, Callable

from ..consts.graphics import Color


class UI:
    def __init__(self) -> None:
        self.master = None
        self.keys_down = {}
        self.keys_wait = {}
        self.got_release = None

    def init_ui(
        self,
        width: int = 640,
        height: int = 480,
        color: str = Color.BLACK,
        title: str = "Graphics Window",
    ) -> None:
        if self.master is not None:
            self.master.destroy()

        self.canvas_ys = self.canvas_y = height - 1
        self.canvas_xs = self.canvas_x = width - 1

        self.master = tkinter.Tk()
        self.master.protocol("WM_DELETE_WINDOW", exit)
        self.master.title(title)
        self.master.resizable(0, 0)

        self.bg_color = color
        try:
            self.canvas = tkinter.Canvas(
                self.master, width=width, height=height
            )
            self.canvas.pack()
            self.draw_background()
            self.canvas.update()
        except:
            raise Exception("Can not create canvas to draw on")

        self.master.bind("<KeyPress>", self.__key_press)
        self.master.bind("<KeyRelease>", self.__key_release)
        self.__clear_keys()

    def draw_background(self) -> None:
        corners = [
            (0, 0),
            (0, self.canvas_ys),
            (self.canvas_xs, self.canvas_ys),
            (self.canvas_xs, 0),
        ]
        self.polygon(
            corners,
            self.bg_color,
            fill_color=self.bg_color,
            filled=True,
            smoothed=False,
        )

    def refresh(self) -> None:
        self.canvas.update_idletasks()

    def sleep(self, seconds: int) -> None:
        if self.master is None:
            time.sleep(seconds)
        else:
            self.master.update_idletasks()
            pause_time = int(1e3 * seconds)
            self.master.after(pause_time, self.master.quit)
            self.master.mainloop()

    def end_graphics(self) -> None:
        try:
            self.sleep(seconds=1)
            if self.master is not None:
                self.master.destroy()
        finally:
            self.master = None
            self.canvas = None
            self.mouse_enabled = 0
            self.__clear_keys()

    def edit(self, id: int, **kwargs):
        self.canvas.itemconfigure(id, **kwargs)

    def polygon(
        self,
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
        polygon = self.canvas.create_polygon(
            coord_list,
            outline=outline_color,
            fill=fill_color,
            smooth=smoothed,
            width=width,
        )
        if behind > 0:
            self.canvas.tag_lower(polygon, behind)
        return polygon

    def circle(
        self,
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
        return self.canvas.create_arc(
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

    def move_circle(
        self,
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

        self.edit(id, start=end_x, extent=end_y - end_x)
        self.move_to(id, x1, y1)

    def line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        color: str = Color.BLACK,
        width: int = 2,
    ) -> int:
        return self.canvas.create_line(*start, *end, fill=color, width=width)

    def remove_from_screen(
        self,
        x: float,
        fn: Optional[Callable] = None,
        param: int = tkinter._tkinter.DONT_WAIT,
    ) -> None:
        self.canvas.delete(x)
        if fn is None:
            fn = lambda arg: self.master.dooneevent(arg)
        fn(param)

    def move_to(
        self,
        object,
        x: float,
        y: Optional[float] = None,
        fn: Optional[Callable] = None,
        param: int = tkinter._tkinter.DONT_WAIT,
    ) -> None:
        if y is None:
            try:
                x, y = x
            except:
                raise Exception("Invalid coordinates")

        new_coords = []
        current_x, current_y = self.canvas.coords(object)[0:2]
        horizontal = True

        for coord in self.canvas.coords(object):
            add = x - current_x if horizontal else y - current_y
            horizontal = not horizontal
            new_coords.append(coord + add)

        self.canvas.coords(object, *new_coords)
        if fn is None:
            fn = lambda arg: self.master.dooneevent(arg)
        fn(param)

    def __key_press(self, event: tkinter.Event) -> None:
        self.keys_down[event.keysym] = 1
        self.keys_wait[event.keysym] = 1
        self.got_release = None

    def __key_release(self, event: tkinter.Event) -> None:
        try:
            del self.keys_down[event.keysym]
        except:
            pass
        self.got_release = 1

    def __clear_keys(self, event: Optional[tkinter.Event] = None) -> None:
        self.keys_down = {}
        self.keys_wait = {}
        self.got_release = None

    def keys_pressed(
        self,
        fn: Optional[Callable] = None,
        param: int = tkinter._tkinter.DONT_WAIT,
    ) -> list:
        if fn is None:
            fn = lambda arg: self.master.dooneevent(arg)
        fn(param)
        if self.got_release != 0:
            fn(param)
        return self.keys_down.keys()

    def keys_waiting(self) -> dict:
        keys = self.keys_wait.keys()
        self.keys_wait = {}
        return keys

    def text(
        self,
        position: tuple[float, float],
        color: str,
        contents: str,
        font: str = "Helvetica",
        size: int = 12,
        style: str = "normal",
        anchor: str = "nw",
    ) -> int:
        x, y = position
        font = (font, str(size), style)
        return self.canvas.create_text(
            x, y, fill=color, text=contents, font=font, anchor=anchor
        )

    def change_text(
        self,
        id: int,
        new_text: str,
        font: Optional[str] = None,
        size: int = 12,
        style: str = "normal",
    ):
        self.canvas.itemconfigure(id, text=new_text)
        if font is not None:
            self.canvas.itemconfigure(id, font=(font, "-%d" % size, style))

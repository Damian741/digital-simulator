from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from config import GRID_WIDTH


class UpdateRelativeRectMixin:
    def bind_rectangle(self):
        self.bind(size=self.update_rect_size)

    def update_rect_size(self, widget, size):
        self.rectangle.size = size


class UpdateFloatRectMixin(UpdateRelativeRectMixin):
    def bind_rectangle(self):
        super().bind_rectangle()
        self.bind(pos=self.update_rect_pos)

    def update_rect_pos(self, widget, pos):
        self.rectangle.pos = pos


class ColumnName(Label, UpdateRelativeRectMixin):
    def __init__(self, name, bcolor=(1, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.bcolor = bcolor

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bcolor)
            Rectangle(pos=self.pos, size=self.size)

    def print(self, msg):
        self.text = f"{self.name}: {msg}"


class GridUtil:
    def _get_grid_x_y(self, x, y):
        return self._get_grid_cord(x), self._get_grid_cord(y)

    def _get_grid_cord(self, cord):
        return cord // GRID_WIDTH * GRID_WIDTH + GRID_WIDTH / 2

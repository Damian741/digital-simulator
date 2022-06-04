from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.graphics import Line, Color, Rectangle

from .util import ColumnName, UpdateRelativeRectMixin, GridUtil
from config import GRID_WIDTH, LINE_WIDTH, DRAW_GRID


class GridRelativeLayoutCord(RelativeLayout, GridUtil):
    def _validate_x_y(self, x, y, padding_x=0, padding_y=0):
        if x > self.width - padding_x:
            x = self.width - padding_x
        if x < 0 + padding_x:
            x = 0 + padding_x
        if y > self.height - padding_y:
            y = self.height - padding_y
        if y < 0 + padding_y:
            y = 0 + padding_y
        return x, y

    def get_grid_validated_local_cord(self, x, y):
        return self._get_grid_x_y(*self._validate_x_y(*self.to_local(x, y)))


class MiddleLayout(BoxLayout):
    def __init__(self, bottom_layout, **kwargs):
        super().__init__(**kwargs)
        self.left_connectors = ConnectorBar(bottom_layout)
        self.board = Board(bottom_layout)
        self.right_connectors = ConnectorBar(reverse=True)
        self.add_widget(self.left_connectors)
        self.add_widget(self.board)
        self.add_widget(self.right_connectors)


class ConnectorBar(GridRelativeLayoutCord, UpdateRelativeRectMixin):
    def __init__(self, bottom_layout=None, reverse=False, **kw):
        super().__init__(**kw)
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)
            self.rectangle = Rectangle(size=self.size)
        self.bind_rectangle()
        self.reverse = reverse
        # self.connectors = []
        self.connector = None
        self.padding_y = 20
        if bottom_layout:
            Window.bind(mouse_pos=self.mouse_pos)
            self.label = ColumnName(
                text="(x,y)", name="ConnectorBar", bcolor=(1, 0, 0, 1)
            )
            bottom_layout.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # x, y = self._get_grid_x_y(*self.to_local(*touch.pos))
            x, y = self.to_local(*touch.pos)
            x, y = self._validate_x_y(x, y)
            x, y = self.get_grid_validated_local_cord(*touch.pos)
            if touch.button == "left":  # left mouse button
                if not self.connector:
                    self.connector = Connector(
                        center_y=y, width=self.width, reverse=self.reverse
                    )
                    self.connector.center_y = y
                    self.add_widget(self.connector)
                else:
                    self.connector.center_y = y
            elif touch.button == "right" and self.connector:
                self.remove_widget(self.connector)
                self.connector = None

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == "left" and self.connector:
                x, y = self.to_local(*touch.pos)
                x, y = self._validate_x_y(x, y)
                x, y = self.get_grid_validated_local_cord(*touch.pos)
                self.connector.center_y = y

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # if touch.grab_current is self:
            # touch.ungrab(self)
            if self.connector:
                x, y = self.to_local(*touch.pos)
                x, y = self._validate_x_y(x, y)
                x, y = self.get_grid_validated_local_cord(*touch.pos)
                self.connector.center_y = y

    def _validate_x_y(self, x, y):
        return super()._validate_x_y(x, y, padding_y=self.padding_y)

    def mouse_pos(self, window, pos):
        self.label.print(self.to_local(*pos))


class Connector(Layout):
    def __init__(self, reverse=False, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)
            self.rectangle = (
                Rectangle(pos=[self.x, self.y], size=[self.width / 2, self.height])
                if reverse
                else Rectangle(
                    pos=[self.width / 2, self.y], size=[self.width / 2, self.height]
                )
            )
            Color(1, 0.2, 0.2, 1)
            self.line = Line(
                points=[
                    self.width / 2,
                    self.y + self.height / 2,
                    self.width,
                    self.y + self.height / 2,
                ],
                width=5,
            )
        self.bind(pos=self.update_canvas)

    def update_canvas(self, widget, pos):
        old_rect_pos = self.rectangle.pos
        self.rectangle.pos = (old_rect_pos[0], pos[1])
        old_points = self.line.points
        self.line.points = [
            old_points[0],
            pos[1] + self.height / 2,
            old_points[2],
            pos[1] + self.height / 2,
        ]


class Board(GridRelativeLayoutCord):
    def __init__(self, bottom_layout, **kwargs):
        super().__init__(**kwargs)
        self.bottom_layout = bottom_layout
        Window.bind(mouse_pos=self.mouse_pos)
        self.padding_y = 5
        self.label = ColumnName(text="(x, y)", name="GlobalCord", bcolor=(0, 1, 0, 0.5))
        self.local_label = ColumnName(
            text="(x, y)", name="LocalBoardCord", bcolor=(0, 0, 1, 0.5)
        )
        self.bottom_layout.add_widget(self.label)
        self.bottom_layout.add_widget(self.local_label)
        # self.add_widget(self.local_label)
        self.drawed_lines = []
        self.last_line = None
        if DRAW_GRID:
            self.horizontal_grid = []
            self.vertical_grid = []
            self.bind(size=self.update_grid)

    def update_grid(self, *args):
        for y in range(0, len(self.vertical_grid)):
            self.vertical_grid[y].points = [
                0,
                y * GRID_WIDTH,
                self.width,
                y * GRID_WIDTH,
            ]
        for x in range(0, len(self.horizontal_grid)):
            self.horizontal_grid[x].points = [
                x * GRID_WIDTH,
                0,
                x * GRID_WIDTH,
                self.height,
            ]

        with self.canvas:
            Color(1, 1, 1, 1)
            # add more grid if need
            for y in range(len(self.vertical_grid), int(self.height / GRID_WIDTH)):
                self.vertical_grid.append(
                    Line(points=[0, y * GRID_WIDTH, self.width, y * GRID_WIDTH])
                )
            for x in range(len(self.horizontal_grid), int(self.width / GRID_WIDTH)):
                self.horizontal_grid.append(
                    Line(points=[x * GRID_WIDTH, 0, x * GRID_WIDTH, self.height])
                )

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return

        if touch.button == "left":  # left mouse button
            if self.last_line:  # stop drawing last line
                # TODO check if line is drawed in cardinal direction,
                # TODO handle situation when there is already end of line, or another line
                if self.last_line not in self.drawed_lines:
                    self.drawed_lines.append((self.last_line, self.line_color))
                self.last_line = None
            else:
                x, y = self.get_grid_validated_local_cord(*touch.pos)
                # search if there already is line
                for child, color in self.drawed_lines:
                    x1, y1 = child.points[:2]
                    x2, y2 = child.points[-2:]
                    if x2 < x + 10 and x2 > x - 10 and y2 < y + 10 and y2 > y - 10:
                        color.rgb = (1, 0, 0)
                        self.last_line = child
                        return
                    elif x1 < x + 10 and x1 > x - 10 and y1 < y + 10 and y1 > y - 10:
                        color.rgb = (1, 0, 0)
                        self.last_line = child
                        points = self.last_line.points
                        # reverse points
                        points[:2] = [x2, y2]
                        middle1 = points[2:4]
                        middle2 = points[4:6]
                        points[2:4] = middle2
                        points[4:6] = middle1
                        points[-2:] = [x1, y1]
                        self.last_line.points = points
                        return

                with self.canvas:
                    self.line_color = Color(0, 1, 0, 1)
                    self.last_line = Line(
                        points=[x, y, x, y, x, y, x, y], width=LINE_WIDTH
                    )

        elif touch.button == "right":  # right mouse button
            if self.last_line:
                self.canvas.remove(self.last_line)
                if self.last_line in self.drawed_lines:
                    self.drawed_lines.remove(self.last_line)
                self.last_line = None

    def mouse_pos(self, window, pos):
        self.label.print(pos)
        pos = self.get_grid_validated_local_cord(*pos)
        self.local_label.print(pos)
        if self.last_line:
            last_pos = self.last_line.points
            x1, y1 = last_pos[:2]
            x2, y2 = last_pos[-2:]
            tan_a = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else 0
            if tan_a >= -1 and tan_a < 1:
                middle_x = self._get_grid_cord((x2 - x1) / 2 + x1)
                last_pos[2:6] = [middle_x, y1, middle_x, y2]
            else:
                middle_y = self._get_grid_cord((y2 - y1) / 2 + y1)
                last_pos[2:6] = [x1, middle_y, x2, middle_y]
            last_pos[-2:] = pos
            self.last_line.points = last_pos

    def _validate_x_y(self, x, y):
        return super()._validate_x_y(x, y, padding_y=self.padding_y)

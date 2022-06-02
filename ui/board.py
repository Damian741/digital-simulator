from math import ceil
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color

from .util import ColumnName
from config import GRID_WIDTH, LINE_WIDTH

def get_grid_cord(cord):
    return cord // GRID_WIDTH * GRID_WIDTH + GRID_WIDTH / 2


class Board(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.label = ColumnName(pos=(0,0),  size_hint=[None, None], size=(100, 20), text="(x, y)")
        self.local_label = ColumnName(pos=(200,0),  size_hint=[None, None], size=(200, 20), text="(x, y)")
        self.add_widget(self.label)
        self.add_widget(self.local_label)
        self.drawed_lines = []
        self.last_line = None
        self.horizontal_grid = []
        self.vertical_grid = []
        self.bind(size=self.update_grid)
    
    def draw_grid(self):
        with self.canvas:
            Color(1, 1, 1, 1)
            for y in range(0, ceil(self.height/GRID_WIDTH)):
                self.vertical_grid.append(Line(points=[0, y*GRID_WIDTH, self.width, y*GRID_WIDTH]))
            for x in range(0, ceil(self.width/GRID_WIDTH)):
                self.horizontal_grid.append(Line(points=[x*GRID_WIDTH, 0, x*GRID_WIDTH, self.height]))
    
    def update_grid(self, *args):
        for y in range(0, len(self.vertical_grid)):
            self.vertical_grid[y].points = [0, y*GRID_WIDTH, self.width, y*GRID_WIDTH]
        for x in range(0, len(self.horizontal_grid)):
            self.horizontal_grid[x].points = [x*GRID_WIDTH, 0, x*GRID_WIDTH, self.height]

        with self.canvas:
            Color(1, 1, 1, 1)
            # add more grid if need
            for y in range(len(self.vertical_grid), ceil(self.height/GRID_WIDTH)):
                self.vertical_grid.append(Line(points=[0, y*GRID_WIDTH, self.width, y*GRID_WIDTH]))
            for x in range(len(self.horizontal_grid), ceil(self.width/GRID_WIDTH)):
                    self.horizontal_grid.append(Line(points=[x*GRID_WIDTH, 0, x*GRID_WIDTH, self.height]))

    def on_touch_down(self, touch):
        if touch.button == "left":  # left mouse button
            if self.last_line:  # stop drawing last line
                if self.last_line not in self.drawed_lines:
                    self.drawed_lines.append(self.last_line)
                self.last_line = None
            else:
                x, y = self.to_local(*touch.pos)
                if x > self.width:
                    x = self.width
                if y > self.height:
                    y = self.height
                x = get_grid_cord(x)
                y = get_grid_cord(y)
                # search if there already is line
                for child in self.drawed_lines:
                    if isinstance(child, Line):
                        x1, y1 = child.points[:2]
                        x2, y2 = child.points[-2:]
                        if x2 < x + 10 and x2 > x - 10 and y2 < y + 10 and y2 > y - 10:
                            self.last_line = child
                            return
                        elif x1 < x + 10 and x1 > x - 10 and y1 < y + 10 and y1 > y - 10:
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
                    self.last_line = Line(points=[x, y, x, y, x, y, x, y], width=LINE_WIDTH)

        elif touch.button == "right":  # right mouse button
            if self.last_line:
                self.canvas.remove(self.last_line)
                if self.last_line in self.drawed_lines:
                    self.drawed_lines.remove(self.last_line)
                self.last_line = None

    def mouse_pos(self, window, pos):
        self.label.text = str(pos)
        x, y = pos
        if x > self.width:
            x = self.width
        if y > self.height:
            y = self.height
        x = get_grid_cord(x)
        y = get_grid_cord(y)
        pos = (x, y)
        self.local_label.text = str(pos)
        if self.last_line:
            last_pos = self.last_line.points
            x1, y1 = last_pos[:2]
            x2, y2 = last_pos[-2:]
            tan_a = (y2-y1)/(x2-x1) if x2-x1 !=0 else 0
            if tan_a >=-1 and tan_a < 1:
                middle_x = get_grid_cord((x2 - x1)/2 + x1)
                last_pos[2:6] = [middle_x, y1, middle_x, y2]
            else:
                middle_y = get_grid_cord((y2 - y1)/2 + y1)
                last_pos[2:6] = [x1, middle_y, x2, middle_y]
            last_pos[-2:] = pos
            self.last_line.points=last_pos
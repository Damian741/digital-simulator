from math import ceil
from tkinter import Grid
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Line, Color

LINE_WIDTH = 5
GRID_WIDTH = 11

def get_grid_cord(cord):
    return cord // GRID_WIDTH * GRID_WIDTH + GRID_WIDTH / 2

class ColumnName(Label):
    pass


class MainScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.size_hint = [1, 1]
        self.height = Window.height
        self.width = Window.width
        self.label = ColumnName(pos=(0,0),  size_hint=[None, None], size=(100, 20), text="(x, y)")
        self.add_widget(self.label)
        self.drawed_lines = []
        self.last_line = None
        self.draw_grid()
    
    def draw_grid(self):
        with self.canvas:
            Color(1, 1, 1, 1)
            for y in range(0, ceil(self.height/GRID_WIDTH)):
                Line(points=[0, y*GRID_WIDTH, self.width, y*GRID_WIDTH])

            for x in range(0, ceil(self.width/GRID_WIDTH)):
                Line(points=[x*GRID_WIDTH, 0, x*GRID_WIDTH, self.height])

    def on_touch_down(self, touch):
        if touch.button == "left":  # left mouse button
            if self.last_line:  # stop drawing last line
                if self.last_line not in self.drawed_lines:
                    self.drawed_lines.append(self.last_line)
                self.last_line = None
            else:
                x, y = touch.pos
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
        x = get_grid_cord(x)
        y = get_grid_cord(y)
        pos = (x, y)
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
            

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    Config.set("graphics", "width", "1000")
    Config.set("graphics", "height", "800")
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    Config.write()
    MainApp().run()
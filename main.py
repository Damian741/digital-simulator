from turtle import position
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Line, Color

class ColumnName(Label):
    pass


class MainScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.label = ColumnName(pos=(0,0),  size_hint=[None, None], size=(100, 20), text="(x, y)")
        self.add_widget(self.label)
        self.last_line = None

    def on_touch_down(self, touch):
        if self.last_line:
            self.last_line = None
        else:
            x, y = touch.pos
            with self.canvas:
                self.line_color = Color(0, 1, 0, 1)
                self.last_line = Line(points=[x, y, x, y, x, y, x, y], width=5)


    def mouse_pos(self, window, pos):
        self.label.text = str(pos)
        if self.last_line:
            last_pos = self.last_line.points
            x1, y1 = last_pos[:2]
            x2, y2 = last_pos[-2:]
            tan_a = (y2-y1)/(x2-x1) if x2-x1 !=0 else 0
            if tan_a >=-1 and tan_a < 1:
                middle_x = (x2 - x1)/2 + x1
                last_pos[2:6] = [middle_x, y1, middle_x, y2]
            else:
                middle_y = (y2 - y1)/2 + y1
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
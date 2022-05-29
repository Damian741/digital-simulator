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
                self.last_line = Line(points=[x, y, x, y], width=5)


    def mouse_pos(self, window, pos):
        self.label.text = str(pos)
        if self.last_line:
            last_pos = self.last_line.points
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
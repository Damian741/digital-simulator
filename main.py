from kivy.app import App
from kivy.config import Config


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from kivy.graphics import Line

class MainScreen(FloatLayout):
    def on_touch_up(self, touch):
        # touch.opos - start position
        # touch.pos - end position
        with self.canvas:
            Line(points=[touch.opos[0], touch.opos[1], touch.pos[0], touch.pos[1]])

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    Config.set("graphics", "width", "1000")
    Config.set("graphics", "height", "800")
    Config.write()
    MainApp().run()
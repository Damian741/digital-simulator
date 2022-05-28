from kivy.app import App
from kivy.config import Config

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Hello world"))

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    Config.set("graphics", "width", "1000")
    Config.set("graphics", "height", "800")
    Config.write()
    MainApp().run()
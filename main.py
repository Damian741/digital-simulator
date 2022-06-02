from kivy.app import App
from kivy.config import Config
from ui.main_screen import MainScreen
            

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    # Config.set("graphics", "width", "1000")
    # Config.set("graphics", "height", "800")
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    Config.write()
    MainApp().run()
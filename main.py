from kivy.app import App
from kivy.config import Config
from ui.mainscreen import MainScreen
            

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    Config.set("graphics", "width", "2000")
    Config.set("graphics", "height", "1200")
    Config.set('graphics', 'resizable', False)
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    Config.write()
    MainApp().run()
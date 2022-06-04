from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from .toplayout import TopNavbar
from .middlelayout import MiddleLayout
from .bottomlayout import BottomLayout

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_navbar = TopNavbar()
        self.bottom_layout = BottomLayout()
        self.board = MiddleLayout(self.bottom_layout)
        self.add_widget(self.top_navbar)
        self.add_widget(self.board)
        self.add_widget(self.bottom_layout)
        
from kivy.uix.boxlayout import BoxLayout

from .top_navbar import TopNavbar
from .board import Board

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_navbar = TopNavbar(size_hint=(1, 0.2))
        self.board = Board(size_hint=(1, 0.8))
        self.add_widget(self.top_navbar)
        self.add_widget(self.board)
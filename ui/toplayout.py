from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle

from .util import UpdateRelativeRectMixin

class TopNavbar(RelativeLayout, UpdateRelativeRectMixin):
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas:
            Color(0, 1, 0, 0.1)
            self.rectangle = Rectangle(size=self.size)
        self.bind_rectangle()
        #self.bind(size=self.update_rect)
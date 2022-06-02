from kivy.uix.label import Label

class ColumnName(Label):
    pass


class UpdateFloatRectMixin:
    def update_rect(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size


class UpdateRelativeRectMixin:
    def update_rect(self, *args):
        self.rectangle.size = self.size
from pygame import Surface
from const import DRAW_SCREEN_SIZE

class Engine():
    def __init__(self):
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)

    def render(self, game):
        self.draw_screen.fill((0, 0, 0))
        return self.draw_screen
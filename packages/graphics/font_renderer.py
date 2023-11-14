from pygame.font import Font
from pygame import Surface
from .const import FONT_COLOR, FONT_SIZE

class FontRenderer:
    def __init__(self):
        self.__fonts = {
            name: Font('./packages/graphics/font.ttf', size)
            for name, size in FONT_SIZE.items()
        }

    def render(self, text: str, size: str) -> Surface:
        return self.__fonts[size].render(text, False, FONT_COLOR)

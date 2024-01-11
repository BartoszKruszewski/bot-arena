from pygame import Surface
from pygame.font import Font
from .gui_element import GUIElement
from packages import ASSETS_DIRECTORY

class Text(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], text: str, **kwargs):
        super().__init__(pos, size, **kwargs)

        self.properties['text'] = text
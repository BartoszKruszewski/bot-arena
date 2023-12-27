from pygame import Surface
from pygame.font import Font
from .gui_element import GUIElement
from packages import ASSETS_DIRECTORY

class Text(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.font = Font(
            f'{ASSETS_DIRECTORY}/{self.properties.get("font", "font_gui")}.ttf',
            self.properties.get('font_size', 8)
        )

    def render(self) -> Surface:
        return self.font.render(
                self.properties.get('text', ""),
                True,
                self.properties.get('color', (0, 0, 0))
        )
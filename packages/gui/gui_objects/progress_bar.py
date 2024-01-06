from pygame import Surface, Rect
from .gui_element import GUIElement

class ProgressBar(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['state'] = 0
        self.properties['background_color'] = kwargs.get('background_color', (10, 10, 10))
        self.properties['color'] = kwargs.get('background_color', (255, 255, 255))

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties['background_color'])
        surf.fill(
            self.properties['color'],
            Rect(
                0, 0,
                self.properties['state'] * self.real_size.x,
                self.real_size.y
            ))
        return surf
from .gui_element import GUIElement
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event as pgevent

class RadioButton(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['active'] = self.properties.get('active', False)

        self.on_click = self.properties.get('on_click', lambda: None)
        self.active_color = self.properties.get('active_color', (255, 255, 255))
        self.color = self.properties.get('color', (0, 0, 0))

    def update(self, dt):
        super().update(dt)
        if self.is_clicked():
            self.on_click()
            self.properties['active'] = not self.properties['active']               

    def render(self):
        self.properties['color'] = self.active_color if self.properties['active'] else self.color
        return super().render()


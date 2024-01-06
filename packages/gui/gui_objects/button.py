from .gui_element import GUIElement
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event as pgevent, Event

class Button(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.on_click = self.properties.get('on_click', lambda: None)
        self.properties['blocked'] = self.properties.get('blocked', False)
        self.blocked_color = self.properties.get('blocked_color', (20, 20, 20))
        self.color = self.properties.get('color', (0, 0, 0))

    def update(self, dt):
        super().update(dt)

    def handle_event(self, event: pgevent) -> None:
        if not self.properties.get('blocked', False):
            if self.is_clicked(event):
                self.on_click(*self.properties.get('args', ()))

    def render(self):
        self.properties['color'] = self.blocked_color if self.properties['blocked'] else self.color 
        return super().render()
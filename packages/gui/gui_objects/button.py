from .gui_element import GUIElement
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event as pgevent, Event

class Button(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.on_click = self.properties.get('on_click', lambda: None)

    def update(self, dt):
        super().update(dt)

    def handle_event(self, event: pgevent) -> None:
        if self.is_clicked(event):
            self.on_click()
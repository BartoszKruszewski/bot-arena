from ..gui_object import GUIElement
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event as pgevent

class Button(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.on_click = self.properties.get('on_click', lambda: None)

    def handle_event(self, event: pgevent) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if self.global_pos.x < event.pos[0] < self.global_pos.x + self.real_size.x:
                if self.global_pos.y < event.pos[1] < self.global_pos.y + self.real_size.y:
                    self.on_click()
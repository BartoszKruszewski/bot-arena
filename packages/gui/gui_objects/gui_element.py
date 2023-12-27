from abc import ABC
from .gui_object import GUIobject
from pygame.event import Event
from pygame import Surface, font, MOUSEBUTTONDOWN, BUTTON_LEFT
from pygame.mouse import get_pos, get_pressed

class GUIElement(GUIobject, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)
        self.properties['fontSize'] = self.properties.get('fontSize', 30)

    def handle_event(self, event: Event) -> None:
        pass

    def update(self, dt):
        pass

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        surf.blit(
            font.SysFont('arial', self.properties['fontSize']).render(self.properties.get('text', ""), True, (0, 0, 0)),
            (self.real_size.x / 2 - 30, self.real_size.y / 2 - 15)
        )
        return surf

    def in_mouse_range(self, event_or_none: Event = None) -> bool:
        if event_or_none is None:
            mouse_pos = get_pos()
        else:
            if event_or_none.type != MOUSEBUTTONDOWN:
                raise Exception("Event type is not MOUSEBUTTONDOWN")
            mouse_pos = event_or_none.pos
        return all((
            self.global_pos.x < mouse_pos[0] < self.global_pos.x + self.real_size.x,
            self.global_pos.y < mouse_pos[1] < self.global_pos.y + self.real_size.y
        )) 

    
    def is_clicked(self, event: Event) -> bool:
        if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
            return self.in_mouse_range(event)
        return False

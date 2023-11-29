from abc import ABC
from .gui_object import GUIobject
from pygame.event import Event
from pygame import Surface

class GUIElement(GUIobject, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)

    def handle_event(self, event: Event) -> None:
        pass

    def update(self, dt):
        pass

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        return surf
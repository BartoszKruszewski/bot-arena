from .gui_object import GUIobject
from pygame import Surface
from pygame.event import Event

class Window(GUIobject):
    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        for object in self.sub_objects:
            surf.blit(object.render(), object.real_pos)
        return surf
    
    def handle_event(self, event: Event) -> None:
        for object in self.sub_objects:
            object.handle_event(event)

    def update(self, dt) -> None:
        for object in self.sub_objects:
            object.update(dt)
from .gui_object import GUIobject
from pygame import Surface, Vector2
from pygame.event import Event
from pygame.font import Font
from packages import ASSETS_DIRECTORY

class Window(GUIobject):
    def __init__(self, sub_objects, pos: tuple[float, float], size: tuple[float, float], **kwargs):
            super().__init__(sub_objects, pos, size, **kwargs)
            self.font = Font(
                f'{ASSETS_DIRECTORY}/{self.properties.get("font", "font_gui")}.ttf',
                self.properties.get('font_size', 20)
            )

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        if 'name' in self.properties:
            surf.blit(self.font.render(
                self.properties.get('name', ""),
                True,
                self.properties.get('header_color', (255, 255, 255))), (0, 0))
        for object in self.sub_objects:
            surf.blit(object.render(), object.real_pos)
        return surf
    
    def handle_event(self, event: Event) -> None:
        for object in self.sub_objects:
            object.handle_event(event)

    def update(self, dt) -> None:
        for object in self.sub_objects:
            object.update(dt)
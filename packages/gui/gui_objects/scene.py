from .gui_object import GUIobject
from pygame import Surface, Vector2
from pygame.font import Font
from .window import Window
from pygame.event import Event
from packages.gui.const import HEADER_BAR_SIZE
from packages import ASSETS_DIRECTORY

class Scene(GUIobject):
    def __init__(self, sub_objects: list['GUIobject'], **kwargs):
        super().__init__(sub_objects, (0, 0), (1, 1), **kwargs)
        self.surf = None
        self.font = Font(
                f'{ASSETS_DIRECTORY}/{self.properties.get("font", "font_gui")}.ttf',
                self.properties.get('font_size', 20)
            )

    def get_surf(self) -> Surface:
        return self.surf

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        if 'name' in self.properties:
            surf.blit(self.font.render(
                self.properties.get('name', ""),
                True,
                self.properties.get('header_color', (255, 255, 255))), (0, 0))
        for object in self.sub_objects:
            surf.blit(object.render(), object.real_pos)
        self.surf = surf
        return surf
    
    def calc_pos(self, global_pos: tuple, screen_size: tuple) -> None:
        global_pos = Vector2(global_pos)
        screen_size = Vector2(screen_size)

        self.real_pos = Vector2(
            global_pos.x + screen_size.x * self.pos.x,
            global_pos.y + screen_size.y * self.pos.y 
        )
        self.real_size = Vector2(
            screen_size.x * self.size.x,
            screen_size.y * self.size.y
        )
        self.global_pos = global_pos

        queue = [self]
        while queue != []:
            window = queue.pop(0)
            for object in window.sub_objects:

                object.real_pos = Vector2(
                    window.real_size.x * object.pos.x,
                    ((window.real_size.y - HEADER_BAR_SIZE) * object.pos.y + HEADER_BAR_SIZE)
                )

                object.real_size = Vector2(
                    window.real_size.x * object.size.x,
                    (window.real_size.y - HEADER_BAR_SIZE) * object.size.y
                )

                object.global_pos = window.global_pos + object.real_pos
                if isinstance(object, Window):
                    queue.append(object)

    def handle_event(self, event: Event) -> None:
        for object in self.sub_objects:
            object.handle_event(event)

    def update(self, dt) -> None:
        for object in self.sub_objects:
            object.update(dt)
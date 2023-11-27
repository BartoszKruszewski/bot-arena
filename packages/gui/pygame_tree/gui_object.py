from pygame import Vector2, Surface, Color
from pygame import event as pgevent
from abc import ABC

class GUIobject(ABC):
    def __init__(self, sub_objects: list['GUIobject'], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        self.sub_objects = sub_objects

        self.pos = Vector2(pos)
        self.size = Vector2(size)

        self.real_pos = None 
        self.real_size = None

        self.global_pos = None

        self.properties = kwargs
    
class Scene(GUIobject):
    def __init__(self, sub_objects: list['GUIobject'], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(sub_objects, pos, size, **kwargs)
        self.surf = None

    def get_surf(self) -> Surface:
        return self.surf

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        for object in self.sub_objects:
            surf.blit(object.render(), object.real_pos)
        self.surf = surf
        return surf
    
    def calc_pos(self, global_pos: tuple, screen_size: tuple) -> None:
        global_pos = Vector2(global_pos)
        screen_size = Vector2(screen_size)

        self.real_pos = Vector2(global_pos.x + screen_size.x * self.pos.x, global_pos.y + screen_size.y * self.pos.y)
        self.real_size = Vector2(screen_size.x * self.size.x, screen_size.y * self.size.y)
        self.global_pos = global_pos

        queue = [self]
        while queue != []:
            window = queue.pop(0)
            for object in window.sub_objects:
                object.real_pos = Vector2(window.real_size.x * object.pos.x,window.real_size.y * object.pos.y)
                object.real_size = Vector2(window.real_size.x * object.size.x, window.real_size.y * object.size.y)
                object.global_pos = window.global_pos + object.real_pos
                if isinstance(object, Window):
                    queue.append(object)

    def handle_event(self, event: pgevent) -> None:
        for object in self.sub_objects:
            object.handle_event(event)

class Window(GUIobject):
    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        for object in self.sub_objects:
            surf.blit(object.render(), object.real_pos)
        return surf
    
    def handle_event(self, event: pgevent) -> None:
        for object in self.sub_objects:
            object.handle_event(event)
    
class GUIElement(GUIobject, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)

    def handle_event(self, event: pgevent) -> None:
        pass

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        return surf


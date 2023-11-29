from pygame import Vector2, mouse
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

    def update(self, dt):
        pass

    def in_mouse_range(self) -> bool:
        mouse_pos = mouse.get_pos()
        return all((
                self.global_pos.x < mouse_pos[0] < self.global_pos.x + self.real_size.x,
                self.global_pos.y < mouse_pos[1] < self.global_pos.y + self.real_size.y
            )) 
    
    def is_clicked(self) -> bool:
        return self.in_mouse_range() and mouse.get_pressed()[0]
from pygame import Vector2, Surface, Color, Rect
from abc import ABC
from .mouse import Mouse
from pygame.locals import *

class GUIobject(ABC):
    def __init__(self, sub_objects: list['GUIobject'], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        self.sub_objects = sub_objects
        self.visible = True

        self.pos = Vector2(pos) # 0.0 -> 1.0 realtive to parent size
        self.size = Vector2(size) # 0.0 -> 1.0 realtive to parent size

        self.real_pos = None 
        self.real_size = None
        self.global_pos = None

        self.properties = kwargs

    def get_surface(self, dt: float, mouse: Mouse) -> Surface:
        if self.visible:
            return self.render(dt, mouse)
        return Surface(self.real_size)

    def render(self, dt: float, mouse: Mouse) -> Surface:
        pass

    def calc_pos(self, parent_size: Vector2, parent_global_pos: Vector2) -> None:
        self.real_pos = Vector2(self.pos.x * parent_size.x, self.pos.y * parent_size.y)
        self.real_size = Vector2(self.size.x * parent_size.x, self.size.y * parent_size.y)
        self.global_pos = self.real_pos + parent_global_pos
        if self.sub_objects is not None:
            for object in self.sub_objects:
                object.calc_pos(self.real_size, self.global_pos)

    def calc_square_pos(self, parent_size: Vector2, parent_global_pos: Vector2) -> None:
        self.real_pos = Vector2(self.pos.x * parent_size.x, self.pos.y * parent_size.x)
        self.real_size = Vector2(self.size.x * parent_size.x, self.size.x * parent_size.x)
        self.global_pos = self.real_pos + parent_global_pos
        if self.sub_objects is not None:
            for object in self.sub_objects:
                object.calc_square_pos(self.real_size, self.global_pos)

    def in_mouse_range(self, mouse):
        return all((
            self.global_pos.x <= mouse.pos.x <= self.global_pos.x + self.real_size.x,
            self.global_pos.y <= mouse.pos.y <= self.global_pos.y + self.real_size.y,
        ))

class Window(GUIobject):
    def __init__(self, sub_objects: list[GUIobject], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(sub_objects, pos, size, **kwargs)

    def render(self, dt: float, mouse: Mouse):
        surf = Surface(self.real_size)
        surf.fill(Color(0, 0, 0))
        surf.fill(
            Color(255, 255, 255),
            Rect(1, 1, self.real_size.x - 1, self.real_size.y - 1)
        )
        for object in self.sub_objects:
            surf.blit(object.get_surface(dt, mouse), object.real_pos)   
        return surf

class GUIElement(GUIobject):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)

class RectButton(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.__on_click = self.properties.get('on_click', lambda: None)

    def render(self, dt: float, mouse: Mouse) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(Color(0, 0, 0))
        surf.fill(
            Color(255, 0, 0),
            Rect(1, 1, self.real_size.x - 1, self.real_size.y - 1)
        )
        self.check_click(mouse)
        return surf

    def in_mouse_range(self, mouse: Mouse):
        return all((
            self.global_pos.x <= mouse.pos.x <= self.global_pos.x + self.real_size.x,
            self.global_pos.y <= mouse.pos.y <= self.global_pos.y + self.real_size.y,
        ))

    def check_click(self, mouse: Mouse):
        if self.in_mouse_range(mouse):
            if mouse.left_click:
                self.__on_click()

class SquareButton(RectButton):
    def __init__(self, pos: tuple[float, float], size: float, **kwargs):
        super().__init__(pos, size, **kwargs)
        self.calc_pos = self.calc_square_pos

class GoBackButton(SquareButton):
    def __init__(self, **kwargs):
        super().__init__((0.005, 0.005), 0.03, **kwargs)

        if not 'on_click' in self.properties:
            raise Exception('GoBackButton must have on_click property')
        self.__on_click = self.properties.get('on_click', lambda: None)
        
    def render(self, dt: float, mouse: Mouse) -> Surface:
        surf = super().render(dt, mouse)
        surf.fill(Color(0,255,0))
        return surf


    





    
    
        




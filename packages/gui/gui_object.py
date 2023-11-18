from pygame import Vector2, Surface, Color, Rect
from pygame import event as pgevent, KEYDOWN, K_BACKSPACE, font
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
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('color', (0, 0, 0)))
        return surf

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

    def collect_info(self, info: dict):
        if self.properties.get('collect_info', None) is not None:
            if hasattr(self, 'get_info'):
                info[self.properties['collect_info']] = self.get_info()
            else:
                raise Exception('Object must have get_info method to collect info when collect_info property is set')
        
        if self.sub_objects is not None:
            for object in self.sub_objects:
                object.collect_info(info)

    def in_mouse_range(self, mouse):
        return all((
            self.global_pos.x <= mouse.pos.x <= self.global_pos.x + self.real_size.x,
            self.global_pos.y <= mouse.pos.y <= self.global_pos.y + self.real_size.y,
        ))


class Window(GUIobject):
    def __init__(self, sub_objects: list[GUIobject], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(sub_objects, pos, size, **kwargs)

    def render(self, dt: float, mouse: Mouse):
        surf = super().render(dt, mouse)
        for object in self.sub_objects:
            surf.blit(object.get_surface(dt, mouse), object.real_pos)   
        return surf
        
class GUIElement(GUIobject):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)

class Button(GUIElement, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.__on_click = self.properties.get('on_click', lambda: None)
        self.__out_click = self.properties.get('out_click', lambda: None)

    def render(self, dt: float, mouse: Mouse) -> Surface:
        surf = super().render(dt, mouse)
        text = self.properties.get('text', '')
        surf.blit(
            font.SysFont('arial', 30).render(text, True, Color(0, 0, 0)),
            (self.real_size.x / 2 - 30, self.real_size.y / 2 - 15)
        )
        self.check_click(mouse)
        return surf

    def check_click(self, mouse: Mouse):
        if self.in_mouse_range(mouse):
            if mouse.left_click:
                self.__on_click()
        else:
            if mouse.left_click:
                self.__out_click()

class RectButton(Button):
    pass

class SquareButton(Button):
    def __init__(self, pos: tuple[float, float], size: float, **kwargs):
        super().__init__(pos, size, **kwargs)
        self.calc_pos = self.calc_square_pos

class GoBackButton(SquareButton):
    def __init__(self, **kwargs):
        super().__init__((0.005, 0.005), 0.03, color=(0,255,0), **kwargs)

        if not 'on_click' in self.properties:
            raise Exception('GoBackButton must have on_click property')
        self.__on_click = self.properties.get('on_click', lambda: None)
        
class InputField(Button):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(
            pos, size,
            on_click=self.on_click,
            out_click=self.out_click,
            **kwargs
        )

        self.is_clicked = False
        self.text = ''

    def render(self, dt: float, mouse: Mouse) -> Surface:
        self.check_click(mouse)
        self.check_text()

        surf = Surface(self.real_size)
        if self.is_clicked:
            surf.fill(Color(128, 0, 0))
        else:
            surf.fill(Color(0, 0, 128))

        if self.text == '' and not self.is_clicked:
            self.text = self.properties.get('placeholder', '')

        surf.blit(
            font.SysFont('arial', 30).render(self.text, True, Color(0, 0, 0)),
            (self.real_size.x / 2 - 30, self.real_size.y / 2 - 15)
        )

        return surf

    def get_info(self):
        return self.text
        
    def check_text(self):
        if self.is_clicked:
            for event in pgevent.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def on_click(self):
        if self.is_clicked: return
        self.is_clicked = True
        pgevent.clear()
        self.text = ''

    def out_click(self):
        self.is_clicked = False






    
    
        




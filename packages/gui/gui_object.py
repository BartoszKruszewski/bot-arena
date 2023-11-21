from pygame import Vector2, Surface, Color, Rect
from pygame import event as pgevent, KEYDOWN, K_BACKSPACE, font
from abc import ABC
from .mouse import Mouse
from pygame.locals import *
from .const import SCREEN_SIZE

###
# GUIobject ABC
#   Window
#   GUIElement ABC
#       Button ABC
#           RectButton
#           SquareButton
#           GoBackButton
#       InputField
###

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
    
    def __iter__(self):
        yield self
        if self.sub_objects is not None:
            for object in self.sub_objects:
                yield from object

    def __str__(self):
        return f'{self.__class__.__name__}{self.properties}'

    def print(self, indent: int = 0):
        print(' ' * indent + str(self))
        if self.sub_objects is not None:
            for object in self.sub_objects:
                object.print(indent + 4)

class Window(GUIobject):
    """Window is a GUIobject that can contain other GUIobjects
    
        Args:
            sub_objects (list[GUIobject]): List of GUIobjects that are contained in this Window
            pos (tuple[float, float]): Position of this Window relative to parent size
            size (tuple[float, float]): Size of this Window relative to parent size
            
        Kwargs:
            color (tuple[int, int, int]): Color of this Window
        """
    def __init__(self, sub_objects: list[GUIobject], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(sub_objects, pos, size, **kwargs)

    def render(self, dt: float, mouse: Mouse):
        surf = super().render(dt, mouse)
        for object in self.sub_objects:
            surf.blit(object.get_surface(dt, mouse), object.real_pos)   
        return surf
        
class GUIElement(GUIobject, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)

class Button(GUIElement, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.__on_click = self.properties.get('on_click', lambda: None)
        self.__out_click = self.properties.get('out_click', lambda: None)
        self.is_clicked = False

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
                if self.properties.get('on_click_color', None) is not None:
                    tmp = self.properties['color']
                    self.properties['color'] = self.properties['on_click_color']
                    self.properties['on_click_color'] = tmp
                    self.is_clicked = not self.is_clicked
        else:
            if mouse.left_click:
                self.__out_click()
                if self.properties.get('out_click_color', None) is not None:
                    self.properties['color'] = self.properties['out_click_color']

class RectButton(Button):
    """RectButton is a Button with rectangular shape

    Args:
        pos (tuple[float, float]): Position of this RectButton relative to parent size
        size (tuple[float, float]): Size of this RectButton relative to parent size

        Kwargs:
            color (tuple[int, int, int]): Color of this RectButton
            on_click (function): Function that is called when this RectButton is clicked
            out_click (function): Function that is called when this RectButton is clicked outside
            text (str): Text that is displayed on this RectButton
    """
    pass

class SquareButton(Button):
    """SquareButton is a Button with square shape
    
    Args:
        pos (tuple[float, float]): Position of this SquareButton relative to parent size
        size (float): Size of this SquareButton relative to parent size
        
        Kwargs:
        color (tuple[int, int, int]): Color of this SquareButton
        on_click (function): Function that is called when this SquareButton is clicked
        out_click (function): Function that is called when this SquareButton is clicked outside
        text (str): Text that is displayed on this SquareButton
    """
    def __init__(self, pos: tuple[float, float], size: float, **kwargs):
        super().__init__(pos, size, **kwargs)
        self.calc_pos = self.calc_square_pos

class GoBackButton(SquareButton):
    """GoBackButton is a SquareButton that closes the window when clicked
    
    Args:
        Kwargs:
            on_click (function): Function that is called when this GoBackButton is clicked"""
    def __init__(self, **kwargs):
        super().__init__((0.005, 0.005), 0.03, color=(0,255,0), text="   <", **kwargs)

        if not 'on_click' in self.properties:
            raise Exception('GoBackButton must have on_click property')
        self.__on_click = self.properties.get('on_click', lambda: None)

class SubmitButton(RectButton):
    def __init__(self, **kwargs):
        super().__init__(
            (0.75, 0.85), (0.2, 0.1), 
            text="Submit", 
            color=(50,205,50),
            **kwargs
            )

class InputField(Button):
    """InputField is a Button that can be used to input text

    Args:
        pos (tuple[float, float]): Position of this InputField relative to parent size
        size (tuple[float, float]): Size of this InputField relative to parent size

        Kwargs:
            color (tuple[int, int, int]): Color of this InputField
            placeholder (str): Text that is displayed on this InputField when it is empty
            collect_info (str): Name of the property in the info dict that is collected when this InputField is clicked
    """
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(
            pos, size,
            on_click=self.on_click,
            out_click=self.out_click,
            **kwargs
        )
        self.is_last_clicked = False
        self.text = ''

    def render(self, dt: float, mouse: Mouse) -> Surface:
        self.check_click(mouse)
        self.check_text()

        surf = super().render(dt, mouse)

        if self.text == '' and not self.is_last_clicked:
            self.text = self.properties.get('placeholder', '')

        surf.blit(
            font.SysFont('arial', 30).render(self.text, True, Color(0, 0, 0)),
            (self.real_size.x / 2 - 30, self.real_size.y / 2 - 15)
        )

        return surf

    def get_info(self):
        return self.text
        
    def check_text(self):
        if self.is_last_clicked:
            for event in pgevent.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def on_click(self):
        if self.is_clicked: return
        self.is_last_clicked = True
        pgevent.clear()
        self.text = ''

    def out_click(self):
        self.is_last_clicked = False

class ErrorWindow(Window):
    def __init__(self, error: str, on_click: callable):
        super().__init__(
            [
                RectButton(
                    (0.1, 0.4), (0.8, 0.1),
                    color=(255, 0, 0), 
                    text=error,
                ),
                GoBackButton(
                    on_click=on_click,
                )
            ],
            (0, 0), (1, 1),
        )
        self.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def render(self, dt: float, mouse: Mouse) -> Surface:
        surf = super().render(dt, mouse)
        return surf
    
    
        




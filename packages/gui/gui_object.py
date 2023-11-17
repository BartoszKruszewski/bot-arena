from pygame import Vector2, Surface, Color, Rect
from ..game_render.engine import Engine
from abc import ABC
from ..game_logic.game import Game

class GUIobject(ABC):
    def __init__(self, sub_objects: list['GUIobject'], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        self.sub_objects = sub_objects
        self.visible = True

        self.pos = Vector2(pos) # 0.0 -> 1.0 realtive to parent size
        self.size = Vector2(size) # 0.0 -> 1.0 realtive to parent size

        self.real_pos = None 
        self.real_size = None

        self.properties = kwargs

    def get_surface(self) -> Surface:
        if self.visible:
            return self.render()
        return Surface(self.real_size)

    def render(self) -> Surface:
        pass

    def calc_real_pos(self, parent_size: Vector2) -> None:
        self.real_pos = Vector2(self.pos.x * parent_size.x, self.pos.y * parent_size.y)
        self.real_size = Vector2(self.size.x * parent_size.x, self.size.y * parent_size.y)

        if self.sub_objects is not None:
            for object in self.sub_objects:
                object.calc_real_pos(self.real_size)

class Window(GUIobject):
    def __init__(self, sub_objects: list[GUIobject], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(sub_objects, pos, size, **kwargs)

    def render(self):
        surf = Surface(self.real_size)
        surf.fill(Color(0, 0, 0))
        surf.fill(
            Color(255, 255, 255),
            Rect(1, 1, self.real_size.x - 1, self.real_size.x - 1)
        )
        for object in self.sub_objects:
            surf.blit(object.get_surface(), object.real_pos)   
        return surf

class GUIElement(GUIobject):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(None, pos, size, **kwargs)

class Button(GUIElement):
    def render(self):
        surf = Surface(self.real_size)
        surf.fill(Color(0, 0, 0))
        surf.fill(
            Color(255, 0, 0),
            Rect(1, 1, self.real_size.x - 1, self.real_size.x - 1)
        )
        return surf

class GameRender(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], game: Game, **kwargs):
        super().__init__(pos, size, **kwargs)
        self.__game = Game()
        self.__engine = Engine(self.__game)
        
    def render(self):
        return self.__engine.render(self.__game, 1, False)



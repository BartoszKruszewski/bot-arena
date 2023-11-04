from pygame import Surface
from pygame import Vector2

from .const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, TILE_SIZE
from .camera import Camera
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer
from ..game_logic.game import Game
from .animated_object import AnimatedObject
from .soldier_animated_object import SoldierAnimatedObject
from .object_tracer import ObjectTracer

class Engine():
    def __init__(self, game: Game):
        self.__draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.__assets_loader = AssetsLoader()
        self.__map_renderer = MapRenderer(game)
        self.__object_tracer = ObjectTracer()
        self.__camera = Camera(game.get_map_size())
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + '/' + 'textures'
        self.__assets = self.__assets_loader.load(path, '.png')

        # creating AnimatedObjects
        self.__animated_objects = []

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game)

    def render(self, game: Game) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''
        self.__camera.update()
        self.__object_tracer.update_soldier_animated_objects(game.get_soldiers(), self.__animated_objects)
        self.__update_animated_objects(game.get_path())

        # reset frame
        self.__draw_screen.fill((0, 0, 0))

        # drawing
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())

        self.__draw_animated_objects()
        return self.__draw_screen

    def __update_animated_objects(self, path: list[tuple[int, int]]):
        for animated_object in self.__animated_objects:
            if isinstance(animated_object, SoldierAnimatedObject):
                animated_object.update(path)

    def __draw_animated_objects(self):
        for animated_object in self.__animated_objects:
            self.__draw_animated_object(animated_object)

    def __draw_animated_object(self, object: AnimatedObject) -> None:
        self.__draw(
                    self.__assets[object.type][object.name][object.animation]
                    [object.direction][object.frame], object.real_pos - object.offset
                )

    def __draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.__camera.get_offset().x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.__camera.get_offset().y <= DRAW_SCREEN_SIZE_Y:
            self.__draw_screen.blit(texture, pos + self.__camera.get_offset())
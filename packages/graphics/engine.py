from pygame import Surface
from pygame import Vector2

from .const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, \
    MAP_SIZE_PX, TILE_SIZE
from .camera import Camera
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer
from ..game_logic.game import Game
from .animated_object import AnimatedObject
from .soldier import SoldierAnimatedObject

class Engine():
    def __init__(self, game: Game):
        self.__draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.__assets_loader = AssetsLoader()
        self.__map_renderer = MapRenderer()
        self.__camera = Camera()
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + '/' + 'textures'
        self.__assets = self.__assets_loader.load(path, '.png')

        # creating AnimationObjects
        self.soldier_animation_objects = [
            SoldierAnimatedObject(Vector2(cord), 'swordsman')
            for side in game.get_soldiers()
            for cord in game.get_soldiers()[side]
        ]

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game.get_map())

    def render(self, game: Game) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''
        self.__camera.update()

        # reset frame
        self.__draw_screen.fill((0, 0, 0))

        # drawing
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())

        # draw test soldier
        self.__draw_soldiers()
        return self.__draw_screen

    def __draw_soldiers(self):
        for soldier_animated_object in self.soldier_animation_objects:
            self.__draw_animated_object(soldier_animated_object)

    def __draw_animated_object(self, object: AnimatedObject) -> None:
        self.__draw(
                    self.__assets[object.type][object.name][object.animation]
                    [object.direction][object.frame], object.pos - object.offset
                )

    def __draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.__camera.get_offset().x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.__camera.get_offset().y <= DRAW_SCREEN_SIZE_Y:
            self.__draw_screen.blit(texture, pos + self.__camera.get_offset())
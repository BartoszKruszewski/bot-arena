from pygame import Surface
from pygame import Vector2

from .const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, TILE_SIZE
from .camera import Camera
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer
from ..game_logic.game import Game
from .soldier_rt import SoldierRT
from .soldier_tracer import SoldierTracer

class Engine():
    def __init__(self, game: Game):
        self.__draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.__assets_loader = AssetsLoader()
        self.__map_renderer = MapRenderer(game)
        self.__soldier_tracer = SoldierTracer(game.get_path())
        self.__camera = Camera(game.get_map_size())
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + '/' + 'textures'
        self.__assets = self.__assets_loader.load(path, '.png')

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game)

    def render(self, game: Game) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''
        self.__camera.update()
        self.__soldier_tracer.update(game.get_soldiers())

        # reset frame
        self.__draw_screen.fill((0, 0, 0))

        # drawing
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())
        for soldier in self.__soldier_tracer.get_soldiers():
            self.__draw_soldier(soldier)

        return self.__draw_screen

    def __draw_soldier(self, soldier: SoldierRT) -> None:
        self.__draw(
            self.__assets['soldiers'][soldier.name][soldier.animation]
            [soldier.direction][soldier.frame], soldier.real_pos - soldier.offset
        )
        surf = Surface((1, 1))
        surf.fill((255, 0, 0))
        self.__draw(
            surf, soldier.real_pos
        )

    def __draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.__camera.get_offset().x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.__camera.get_offset().y <= DRAW_SCREEN_SIZE_Y:
            self.__draw_screen.blit(texture, pos + self.__camera.get_offset())
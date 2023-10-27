from pygame import Surface
from pygame import Vector2

from .const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, \
    MAP_SIZE_PX
from .game import Game
from .map import Map
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer

class Engine():
    def __init__(self):
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.assets_loader = AssetsLoader()
        self.map_renderer = MapRenderer()
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + '/' + 'textures'
        self.assets = self.assets_loader.load(path, '.png')
        self.camera_offset = Vector2(0, 0)
        self.map_texture = Surface(MAP_SIZE_PX)
        self.map_rendered = False

    def render(self, game: Game) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''
        if not self.map_rendered:
            self.map_texture = self.map_renderer.render(self.assets, game.map)
            self.map_rendered = True 
        
        # update info
        self.camera_offset = game.camera_offset

        # reset frame
        self.draw_screen.fill((0, 0, 0))

        # drawing
        self.draw_screen.blit(self.map_texture, self.camera_offset)

        return self.draw_screen

    def __draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.camera_offset.x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.camera_offset.y <= DRAW_SCREEN_SIZE_Y:
            self.draw_screen.blit(texture, pos + self.camera_offset)
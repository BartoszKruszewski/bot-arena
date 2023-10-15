from pygame import Surface

from const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y,  TILE_SIZE

from game import Game
from map import Map
from assets_loader import AssetsLoader

from pygame import Vector2

class Engine():
    def __init__(self):
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.load('textures')
        self.camera_offset = Vector2(0, 0)

    def render(self, game: Game) -> Surface:
        self.camera_offset = game.camera_offset
        self.draw_screen.fill((0, 0, 0))
        self.draw_map(game.map)
        return self.draw_screen
    
    def draw_map(self, map: Map) -> None:
        TILE_NAMES = {
            'path': 'tile_path'
        }
        
        for tile_code, cords in map.structures.items():
            for x, y in cords:
                self.draw(
                    self.assets['tiles'][TILE_NAMES[map.get_struct(tile_code)]], 
                    Vector2(x, y) * TILE_SIZE)
                
    def draw(self, texture, pos):
        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.camera_offset.x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.camera_offset.y <= DRAW_SCREEN_SIZE_Y:
            self.draw_screen.blit(texture, pos + self.camera_offset)
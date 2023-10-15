from pygame import Surface

from const import DRAW_SCREEN_SIZE, TILE_SIZE

from game import Game
from map import Map
from assets_loader import AssetsLoader

class Engine():
    def __init__(self):
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.load('textures')

    def render(self, game: Game) -> Surface:
        self.draw_screen.fill((0, 0, 0))
        self.draw_map(game.map)
        return self.draw_screen
    
    def draw_map(self, map: Map) -> None:
        TILE_NAMES = {
            'path': 'tile_path'
        }
        
        for tile_code, cords in map.structures.items():
            for x, y in cords:
                self.draw_screen.blit(
                    self.assets['tiles'][TILE_NAMES[map.get_struct(tile_code)]], 
                    (x * TILE_SIZE, y * TILE_SIZE))
from pygame import Surface
from pygame import Vector2

from const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y,  TILE_SIZE
from game import Game
from map import Map
from assets_loader import AssetsLoader

class Engine():
    def __init__(self):
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.load('textures', '.png')
        self.camera_offset = Vector2(0, 0)

    def render(self, game: Game) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''
        
        # update info
        self.camera_offset = game.camera_offset

        # reset frame
        self.draw_screen.fill((0, 0, 0))

        # drawing
        self.draw_map(game.map)


        return self.draw_screen
    
    def draw_map(self, map: Map) -> None:
        '''Drawing map tiles.
        '''

        TEXTURE_NAMES = {
            'path':  'tile_path',
            'grass': 'tile_grass',
            'trees': 'tile_tree' 
        }
        
        for tile_code, cords in map.structures.items():
            for pos in cords:
                self.draw(
                    self.assets['tiles'][TEXTURE_NAMES[tile_code]], 
                    pos * TILE_SIZE)
                
    def draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.camera_offset.x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.camera_offset.y <= DRAW_SCREEN_SIZE_Y:
            self.draw_screen.blit(texture, pos + self.camera_offset)
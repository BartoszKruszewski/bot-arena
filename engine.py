from pygame import Surface
from pygame import Vector2

from const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, \
    TILE_SIZE, MAP_SIZE_PX
from game import Game
from map import Map
from assets_loader import AssetsLoader

class Engine():
    def __init__(self):
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.load('textures', '.png')
        self.camera_offset = Vector2(0, 0)
        self.map_texture = Surface(MAP_SIZE_PX)
        self.map_rendered = False

    def render(self, game: Game) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''
        if not self.map_rendered:
            self.render_map(game.map)
            self.map_rendered = True 
        
        # update info
        self.camera_offset = game.camera_offset

        # reset frame
        self.draw_screen.fill((0, 0, 0))

        # drawing
        self.draw_screen.blit(self.map_texture, self.camera_offset)


        return self.draw_screen

    def render_map(self, map: Map) -> None:
        '''Drawing map tiles.
        '''

        TEXTURE_NAMES = {
            'path':  'tile_path',
            'grass': 'tile_grass_mid',
            'trees': 'tile_tree' 
        }
        
        for tile_code, cords in map.structures.items():
            for pos in cords:
                if tile_code == 'grass':
                    tile_name = self.get_grass_texture(map, pos)
                else:
                    tile_name = TEXTURE_NAMES[tile_code]
                self.map_texture.blit(self.assets['tiles'][tile_name], pos * TILE_SIZE)
    
    def get_grass_texture(self, map: Map, cord: Vector2):
        SIDES = [Vector2(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        is_path = [(int(v.x), int(v.y)) for v in SIDES if (cord + v in map.structures['path'])]
        sides = []

        if (0, -1) in is_path:
            sides.append('top')
        elif (0, 1) in is_path:
            sides.append('bot')

        if (-1, 0) in is_path:
            sides.append('left')
        elif (1, 0) in is_path:
            sides.append('right')


        if len(sides) == 0:
            if (-1, -1) in is_path:
                sides = ('d1',)
            elif (1, -1) in is_path:
                sides = ('d2',)
            elif (1, 1) in is_path:
                sides = ('d3',)
            elif (-1, 1) in is_path:
                sides = ('d4',)

        sides = tuple(sides)

        TILE_TURNS = {
            (): 'tile_grass_mid',
            ('left',): 'tile_grass_left',
            ('right',): 'tile_grass_right',
            ('bot',): 'tile_grass_bot',
            ('top',): 'tile_grass_top',
            ('bot', 'left'): 'tile_grass_bot_left',
            ('top', 'left'): 'tile_grass_top_left',
            ('bot', 'right'): 'tile_grass_bot_right',
            ('top', 'right'): 'tile_grass_top_right',
            ('d1',): 'tile_grass_d1',
            ('d2',): 'tile_grass_d2',
            ('d3',): 'tile_grass_d3',
            ('d4',): 'tile_grass_d4',
        }

        return TILE_TURNS[sides] if sides in TILE_TURNS.keys() else 'tile_grass_mid'

    def draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.camera_offset.x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.camera_offset.y <= DRAW_SCREEN_SIZE_Y:
            self.draw_screen.blit(texture, pos + self.camera_offset)
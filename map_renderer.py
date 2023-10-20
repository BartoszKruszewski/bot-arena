from pygame import Surface
from pygame import Vector2
from random import choice

from const import MAP_SIZE_PX, TILE_SIZE, MAP_SIZE_X, MAP_SIZE_Y

from map import Map

class MapRenderer:
    def __init__(self) -> None:
        self.map_texture = Surface(MAP_SIZE_PX)
        
    def render(self, assets: dict, map: Map) -> Surface:
        '''Drawing map tiles.
        '''

        TEXTURE_NAMES = {
            'path':  'tile_path',
            'grass': 'tile_grass_mid',
            'farm': 'tile_farm'
        }

        filled_pos = []

        for tile_code, cords in map.structures.items():
            if tile_code != 'obstacles':
                for pos in cords:
                    self.map_texture.blit(
                        assets['tiles'][TEXTURE_NAMES[tile_code]], pos * TILE_SIZE)
                    filled_pos.append(pos)

        grass_pos = [
            Vector2(x, y) 
            for x in range(MAP_SIZE_X)
              for y in range(MAP_SIZE_Y)
                if not Vector2(x, y) in filled_pos
        ]
        
        for pos in grass_pos:
            self.map_texture.blit(
                assets['tiles'][self.__get_grass_turn(map, pos)], pos * TILE_SIZE)

        for cord in sorted(map.structures['obstacles'], key = lambda v: v.y):
            self.__render_obstacle(cord, choice(list(assets['obstacles'].values())))

        return self.map_texture
    
    def __render_obstacle(self, cord: Vector2, texture: Surface) -> None:
        size_x, size_y = texture.get_size()
        render_pos = Vector2(
            cord.x * TILE_SIZE - size_x // 2 + TILE_SIZE // 2,
            cord.y * TILE_SIZE - size_y + TILE_SIZE
        )
        self.map_texture.blit(texture, render_pos)

    def __get_grass_turn(self, map: Map, cord: Vector2) -> str:
        '''Returns name of grass turn based on neighboring tiles.
        '''

        SIDES = [
            Vector2(x, y)
              for x in range(-1, 2)
                for y in range(-1, 2)
        ]

        is_path = [
            (int(v.x), int(v.y))
              for v in SIDES
                if (cord + v in map.structures['path'])]
        
        sides = ''

        sides += 'top' if (0, -1) in is_path else 'bot' if (0, 1) in is_path else ''
        sides += 'left' if (-1, 0) in is_path else 'right' if (1, 0) in is_path else ''

        if not sides:
            if (-1, -1) in is_path:
                sides += 'd1'
            elif (1, -1) in is_path:
                sides += 'd2'
            elif (1, 1) in is_path:
                sides += 'd3'
            elif (-1, 1) in is_path:
                sides += 'd4'

        TILE_TURNS = {
            '': 'tile_grass_mid',
            'left': 'tile_grass_left',
            'right': 'tile_grass_right',
            'bot': 'tile_grass_bot',
            'top': 'tile_grass_top',
            'botleft': 'tile_grass_bot_left',
            'topleft': 'tile_grass_top_left',
            'botright': 'tile_grass_bot_right',
            'topright': 'tile_grass_top_right',
            'd1': 'tile_grass_d1',
            'd2': 'tile_grass_d2',
            'd3': 'tile_grass_d3',
            'd4': 'tile_grass_d4',
        }

        return TILE_TURNS[sides]
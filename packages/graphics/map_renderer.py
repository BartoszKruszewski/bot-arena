from pygame import Surface, SRCALPHA
from pygame import Vector2
from random import choice

from .const import MAP_SIZE_PX, TILE_SIZE, MAP_SIZE_X, MAP_SIZE_Y
from ..game_logic.objects.map import Map

class MapRenderer:
    def __init__(self) -> None:
        self.__map_texture = Surface(MAP_SIZE_PX)
        self.__ground_texture = Surface(MAP_SIZE_PX)
        self.__obstacles_texture = Surface(MAP_SIZE_PX, SRCALPHA)
        self.__assigned_obstacles = []
    
    def __render_ground(self, map: Map, assets: dict):
        '''Drawing map tiles.
        '''

        filled_cords = []

        for cord in map.path:
            self.__ground_texture.blit(assets['tiles']['tile_path'], Vector2(cord) * TILE_SIZE)
            filled_cords.append(cord)

        grass_cords = [
            Vector2(x, y) 
            for x in range(MAP_SIZE_X)
              for y in range(MAP_SIZE_Y)
                if not Vector2(x, y) in filled_cords
        ]
        
        for cord in grass_cords:
            self.__ground_texture.blit(
                assets['tiles']['tile_grass_' + self.__get_grass_turn(cord, map)], cord * TILE_SIZE)

    def __render_obstacles(self, assets: dict) -> None:
        for render_cord, texture_name in sorted(self.__assigned_obstacles, key = lambda x: x[0].y):
            self.__obstacles_texture.blit(assets['obstacles'][texture_name], render_cord)

    def __assign_obstacles(self, cords: list[Vector2], assets: dict):
        obstacle_cords = cords.copy()
        self.__assigned_obstacles = []
        while obstacle_cords:
            render_cord, texture_name, covered_cords = self.__render_obstacle(obstacle_cords[0], assets, obstacle_cords)
            self.__assigned_obstacles.append((render_cord, texture_name))
            for cord in covered_cords:
                obstacle_cords.remove(cord)
    
    def re_render():
        pass

    def render(self, assets: dict, map: Map) -> Surface:
        self.__map_texture = Surface(MAP_SIZE_PX)
        self.__render_ground(map, assets)
        self.__assign_obstacles(map.obstacles, assets)
        self.__render_obstacles(assets)
        self.__map_texture.blit(self.__ground_texture, Vector2(0, 0))

        # self.__draw_obstacles_area(map)

        self.__map_texture.blit(self.__obstacles_texture, Vector2(0, 0))
        
        return self.__map_texture
    
    def __draw_obstacles_area(self, map: Map) -> None:
        surf = Surface((TILE_SIZE, TILE_SIZE))
        surf.fill((255, 0, 0))
        for cord in map.obstacles:
            self.__map_texture.blit(surf, Vector2(cord) * TILE_SIZE)

    def __group_tiles(self, cord: Vector2, other_tiles: list[Vector2]) -> list[Vector2]:
        
        def recursive(actual_cord: Vector2, group: list[Vector2]) -> list[Vector2]:
            new_tiles = [v for v in self.__get_neighbouring_tiles(actual_cord, other_tiles) if v not in group]
            all_tiles = group + new_tiles
            for tile in new_tiles:
                all_tiles.extend(v for v in recursive(tile, all_tiles) if v not in all_tiles)
        
            return all_tiles

        tiles = recursive(cord, []) 
        return tiles
    
    def __get_tile_group_size(self, group: list[Vector2]) -> Vector2:
        max_x = max(group, key = lambda v: v.x).x
        max_y = max(group, key = lambda v: v.y).y
        min_x = min(group, key = lambda v: v.x).x
        min_y = min(group, key = lambda v: v.y).y
        return Vector2(max_x - min_x + 1, max_y - min_y + 1)

    def __get_tile_group_bottom_center(self, group: list[Vector2]) -> Vector2:
        max_x = max(group, key = lambda v: v.x).x
        min_x = min(group, key = lambda v: v.x).x
        max_y = max(group, key = lambda v: v.y).y 
        return Vector2(min_x + (max_x - min_x + 1) / 2, max_y + 1)
        
    def __render_obstacle(self, cord: Vector2, assets: dict, obstacles: list[Vector2]) -> list[Vector2]:
        
        tiles = self.__group_tiles(cord, obstacles)
        tiles_size = self.__get_tile_group_size(tiles) * TILE_SIZE
        size = Vector2(MAP_SIZE_PX) 
        while not (size.x <= tiles_size.x and size.y <= tiles_size.y):
            name = choice(list(assets['obstacles']))
            texture = assets['obstacles'][name]
            size = Vector2(texture.get_size())
        
        bottom_center = self.__get_tile_group_bottom_center(tiles) * TILE_SIZE

        render_pos = Vector2(
            int(bottom_center.x) - size.x // 2,
            int(bottom_center.y - size.y),
        )

        covered_top_left = Vector2(bottom_center.x - size.x // 2, bottom_center.y - size.y)
        covered_bottom_right = Vector2(bottom_center.x + size.x // 2, bottom_center.y)

        covered_cords = [
            cord for cord in tiles if 
                covered_top_left.x // TILE_SIZE <= cord.x <= covered_bottom_right.x // TILE_SIZE and \
                covered_top_left.y // TILE_SIZE <= cord.y <= covered_bottom_right.y // TILE_SIZE
        ]

        return render_pos, name, covered_cords if covered_cords else tiles

    def __get_neighbouring_tiles(self, cord: Vector2, other_tiles: list[Vector2], **kwargs) -> list[Vector2]:
        r = ((x, y) for x in range(-1, 2) for y in range(-1, 2)) \
            if 'diagonal' in kwargs else ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0))

        return [
            Vector2(x, y) + (cord if 'only_offset' not in kwargs else Vector2(0, 0))
                for x, y in r if Vector2(x, y) + cord in other_tiles
        ]

    def __get_grass_turn(self, cord: Vector2, map: Map) -> str:
        '''Returns name of grass turn based on neighboring tiles.
        '''

        is_path = self.__get_neighbouring_tiles(cord, map.path, only_offset = True, diagonal = True)
        
        if not is_path:
            return 'center'

        turn = 'top' if (0, -1) in is_path else 'bot' if (0, 1) in is_path else ''
        turn += 'left' if (-1, 0) in is_path else 'right' if (1, 0) in is_path else ''

        if not turn:
            turn += ([v for key, v in {
                (-1, -1):   'd1',
                (1, -1):    'd2',
                (1, 1):     'd3',
                (-1, 1):    'd4',
            }.items() if key in is_path] + [''])[0]

        return turn
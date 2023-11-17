from pygame import Surface, SRCALPHA, Rect, Vector2, Color
from pygame.draw import rect as draw_rect
from random import choice

from ...game_logic.game import Game
from ..const import TILE_SIZE, SHOW_GRID, SHOW_OBSTACLES_AREA

class MapRenderer:
    '''Map rendering class.
    '''

    def __init__(self, game: Game) -> None:
        self.__map_size = Vector2(game.get_map_size())
        self.__map_texture = Surface(self.__map_size * TILE_SIZE)
        self.__ground_texture = Surface(self.__map_size * TILE_SIZE)
        self.__obstacles_texture = Surface(self.__map_size * TILE_SIZE, SRCALPHA)
        self.__assigned_obstacles = []

    def re_render():
        '''Fast render
        '''
        pass

    def render(self, assets: dict, game: Game) -> Surface:
        '''Complete render.

        Rendering items:
            - path tiles
            - grass
            - obstacles (with pre calculation)
            - map helpers (grid, obstacles area)
        '''

        # reset map texture
        self.__map_texture = Surface(Vector2(game.get_map_size()) * TILE_SIZE)

        # render ground
        self.__render_ground(game.get_path(), assets)
        self.__map_texture.blit(self.__ground_texture, Vector2(0, 0))

        # render obstacles
        self.__assign_obstacles(game.get_obstacles(), assets)
        self.__render_obstacles(assets)

        if SHOW_OBSTACLES_AREA:
            self.__draw_obstacles_area(game.get_obstacles())

        self.__map_texture.blit(self.__obstacles_texture, Vector2(0, 0))

        # render grid
        if SHOW_GRID:
            self.__draw_grid()
        
        return self.__map_texture
    
    def __render_ground(self, path: list[tuple[int, int]], assets: dict):
        '''Drawing map tiles.
        '''

        filled_cords = []

        for cord in path:
            self.__ground_texture.blit(
                self.__randomize_grass(
                    assets['tiles']['path_' + self.__get_path_turn(cord, path)]),
                Vector2(cord) * TILE_SIZE
            )
            filled_cords.append(cord)

        grass_cords = [
            Vector2(x, y) 
            for x in range(int(self.__map_size.x))
              for y in range(int(self.__map_size.y))
                if not Vector2(x, y) in filled_cords
        ]
        
        for cord in grass_cords:
            self.__ground_texture.blit(
                self.__randomize_grass(
                    assets['tiles']['grass']
                ),
                cord * TILE_SIZE
            )
    
    def __get_path_turn(self, cord: Vector2, path: list[tuple[int, int]]) -> str:
        '''Returns name of grass turn based on neighboring tiles.
        '''

        is_path = tuple(
            tuple(v) for v in 
            self.__get_neighbouring_tiles(cord, path, only_offset = True)
            if v != (0, 0)
        )

        CODING = {
            ((1, 0),): 'h',
            ((-1, 0),): 'h',
            ((0, 1),): 'v',
            ((0, -1),): 'v',
            ((-1, 0), (1, 0)): 'h',
            ((0, 1), (0, -1)): 'v',
            ((0, 1), (1, 0)): 'd1',
            ((-1, 0), (0, 1)): 'd2',
            ((0, -1), (-1, 0)): 'd3',
            ((1, 0), (0, -1)): 'd4',
        }

        if is_path not in CODING:
            return CODING[(is_path[1], is_path[0])]
        return CODING[is_path]

    def __render_obstacles(self, assets: dict) -> None:
        '''Rendering obstacles on obstacle texture.
        '''
        for render_cord, texture_name in sorted(self.__assigned_obstacles, key = lambda x: x[0].y):
            self.__obstacles_texture.blit(assets['obstacles'][texture_name], render_cord)

    def __assign_obstacles(self, cords: list[Vector2], assets: dict):
        '''Calculating best textures for obstacles.
        '''
        obstacle_cords = cords.copy()
        self.__assigned_obstacles = []
        while obstacle_cords:
            render_cord, texture_name, covered_cords = self.__render_obstacle(obstacle_cords[0], assets, obstacle_cords)
            self.__assigned_obstacles.append((render_cord, texture_name))
            for cord in covered_cords:
                obstacle_cords.remove(cord)

    def __render_obstacle(
            self, cord: Vector2, assets: dict, obstacles: list[Vector2]
        ) -> tuple[Vector2, str, list[Vector2]]:

        '''Calculate single obstacle texture.

        Returns:
            - position of obstacle
            - texture name
            - covered tiles from group
        '''

        tiles = self.__group_tiles(cord, obstacles)
        tiles_size = self.__get_tile_group_size(tiles) * TILE_SIZE
        size = self.__map_size * TILE_SIZE 
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
        '''Returns neightbouring tile cords.

        Params:
            - only_offset: function returns only offset of neighbouring tiles, not full cords
            - diagonal: function calculate also diagonal neighbouring tiles
        '''

        r = ((x, y) for x in range(-1, 2) for y in range(-1, 2)) \
            if 'diagonal' in kwargs else ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0))

        return [
            Vector2(x, y) + (cord if 'only_offset' not in kwargs else Vector2(0, 0))
                for x, y in r if Vector2(x, y) + cord in other_tiles
        ]

    def __group_tiles(self, cord: Vector2, other_tiles: list[Vector2]) -> list[Vector2]:
        '''Recursive grouping neighbouring tiles.
        '''
        def recursive(actual_cord: Vector2, group: list[Vector2]) -> list[Vector2]:
            new_tiles = [v for v in self.__get_neighbouring_tiles(actual_cord, other_tiles) if v not in group]
            all_tiles = group + new_tiles
            for tile in new_tiles:
                all_tiles.extend(v for v in recursive(tile, all_tiles) if v not in all_tiles)
        
            return all_tiles

        tiles = recursive(cord, []) 
        return tiles

    def __get_tile_group_size(self, group: list[Vector2]) -> Vector2:
        '''Returns max size of grouped tiles bordering rectangle.
        '''
        max_x = max(group, key = lambda v: v.x).x
        max_y = max(group, key = lambda v: v.y).y
        min_x = min(group, key = lambda v: v.x).x
        min_y = min(group, key = lambda v: v.y).y
        return Vector2(max_x - min_x + 1, max_y - min_y + 1)

    def __get_tile_group_bottom_center(self, group: list[Vector2]) -> Vector2:
        '''Returns bottom center of grouped tiles bordering rectangle.
        '''
        max_x = max(group, key = lambda v: v.x).x
        min_x = min(group, key = lambda v: v.x).x
        max_y = max(group, key = lambda v: v.y).y 
        return Vector2(min_x + (max_x - min_x + 1) / 2, max_y + 1)

    def __draw_grid(self):
        '''Draws grid on map texture
        '''

        COLOR = (0, 0, 0, 100)

        surf = Surface((TILE_SIZE, TILE_SIZE), SRCALPHA)
        draw_rect(surf, COLOR, Rect(0, 0, TILE_SIZE, TILE_SIZE), 1)
        for y in range(int(self.__map_size.y)):
            for x in range(int(self.__map_size.x)):
                self.__map_texture.blit(surf, Vector2(x, y) * TILE_SIZE)

    def __draw_obstacles_area(self, obstacles: list[Vector2]) -> None:
        '''Fill in color tiles where are
        obsctales positions in game logic.
        '''

        COLOR = (255, 0, 0)

        surf = Surface((TILE_SIZE, TILE_SIZE))
        surf.fill(COLOR)
        for cord in obstacles:
            self.__map_texture.blit(surf, Vector2(cord) * TILE_SIZE)

    def __randomize_grass(self, texture: Surface) -> Surface:
        '''Radomize grass texture color
        '''
        return self.__randomize_color(
            texture, Color(160, 177, 89),
            [
                Color(160, 177, 89),
                Color(158, 178, 91),
                Color(156, 172, 93),
                Color(164, 181, 86)
            ], 8)

    def __randomize_color(self, texture: Surface, key: Color, colors: list[Color], tolerance: int = 0) -> Surface:
        '''Change key color of texture to random colors from list
        '''
        
        def color_in_tolerance(color: Color):
            return all((
                abs(color.r - key.r) <= tolerance,
                abs(color.g - key.g) <= tolerance,
                abs(color.b - key.b) <= tolerance,
            ))
        
        size_x, size_y = texture.get_size()

        new_texture = texture.copy()
        [
            new_texture.set_at((x, y), choice(colors))
            for x in range(size_x) for y in range(size_y)
            if color_in_tolerance(texture.get_at((x, y)))
        ]
        return new_texture

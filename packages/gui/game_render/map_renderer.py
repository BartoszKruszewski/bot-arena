from pygame import Surface, SRCALPHA, Rect, Vector2, Color
from pygame.draw import rect as draw_rect
from random import choice
from time import sleep
from packages.game_logic.game import Game
from packages.gui.const import TILE_SIZE

class MapRenderer:
    def render(self, assets: dict, game: Game, helpers = []) -> Surface:
        size = Vector2(game.get_map_size())
        self.__map_texture = Surface(size * TILE_SIZE)
        path = game.get_path()

        self.__draw_path(assets, path)
        self.__draw_grass(assets, size, path)
        self.__obstacles_area = self.__get_obstacles_area(size, game.get_obstacles())
        self.__grid = self.__get_grid(size)

        return self.fast_render(helpers)
    
    def fast_render(self, helpers = []) -> Surface:
        
        surf = self.__map_texture.copy()
        if 'obstacles_area' in helpers:
            surf.blit(self.__obstacles_area, (0, 0))
        if 'grid' in helpers:
            surf.blit(self.__grid, (0, 0))

        return surf

    def __draw_path(self, assets, path):
        for pos in path:
            self.__map_texture.blit(
                self.__randomize_grass(
                    assets['tiles']['path_' + self.__get_path_turn(pos, path)]),
                Vector2(pos) * TILE_SIZE
            )

    def __draw_grass(self, assets, size, path):
        for y in range(int(size.y)):
            for x in range(int(size.x)):
                pos = Vector2(x, y)
                if pos not in path:
                    self.__map_texture.blit(
                        self.__randomize_grass(assets['tiles']['grass']),
                        pos * TILE_SIZE
                )

    def __get_path_turn(self, cord: Vector2, path: list[tuple[int, int]]) -> str:
        '''Returns name of grass turn based on neighboring tiles.
        '''

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

        neighbouring = tuple(self.__get_neighbouring_tiles(cord, path))

        if neighbouring in CODING:
            return CODING[neighbouring]
        else:
            neighbouring = neighbouring[1], neighbouring[0]
            if neighbouring in CODING:
                return CODING[neighbouring]
            raise Exception('Invalid path neighbouring!')
    
    def __get_neighbouring_tiles(self, cord: Vector2, other_tiles: list[Vector2]) -> list[Vector2]:
        return [
            (x, y) for x, y in
            ((1, 0), (-1, 0), (0, 1), (0, -1))
            if Vector2(x, y) + cord in other_tiles
        ]

    def __get_grid(self, map_size: Vector2):
        surf = Surface(map_size * TILE_SIZE, SRCALPHA)
        COLOR = (0, 0, 0, 100)

        sq = Surface((TILE_SIZE, TILE_SIZE), SRCALPHA)
        draw_rect(sq, COLOR, Rect(0, 0, TILE_SIZE, TILE_SIZE), 1)
        for y in range(int(map_size.y)):
            for x in range(int(map_size.x)):
                surf.blit(sq, Vector2(x, y) * TILE_SIZE)
        return surf

    def __get_obstacles_area(self, map_size ,obstacles: list[Vector2]):
        surf = Surface(map_size * TILE_SIZE, SRCALPHA)
        COLOR = (255, 0, 0)
        sq = Surface((TILE_SIZE, TILE_SIZE))
        sq.fill(COLOR)
        for obstacle in obstacles:
            surf.blit(sq, Vector2(obstacle.cords) * TILE_SIZE)
        return surf

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

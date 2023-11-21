from random import shuffle, random, choice
import json

from ..stats import MAP_SIZE_X, MAP_SIZE_Y, OBSTACLES_AMOUNT
from .obstalces import Obstacles
class Map():
    def __init__(self, map_path: str) -> None:
        self._start = None
        self._end = None

        self.path = []
        self.obstacles = Obstacles()

        self.MAP_SIZE_X = None
        self.MAP_SIZE_Y = None

        if map_path == None:
            self._start = (0, 0)
            self._end = (MAP_SIZE_X - 1, MAP_SIZE_Y - 1)
            self.MAP_SIZE_X = MAP_SIZE_X
            self.MAP_SIZE_Y = MAP_SIZE_Y
            self.__generate_map()
        else:
            self.__load_map(map_path)

    def __load_map(self, map_path: str) -> None:
        with open(map_path, 'r') as f:
            map_data = json.load(f)

        self.MAP_SIZE_X = map_data['MAP_SIZE_X']
        self.MAP_SIZE_Y = map_data['MAP_SIZE_Y']
        self._start = tuple(map_data['start'])
        self._end = (MAP_SIZE_X - 1, MAP_SIZE_Y - 1)
        self.path = [tuple(pos) for pos in map_data['path']]
        for cord in [tuple(pos) for pos in map_data['obstacles']]:
            self.obstacles.spawn(cord)

    def __generate_path(self, pos) -> None:
        # generate path without loops using backtracking
        if pos in self.path:
            return False
        if pos == self._end:
            return True
        
        if pos[0] < 0 or pos[0] >= MAP_SIZE_X or pos[1] < 0 or pos[1] >= MAP_SIZE_Y:
            return False
        
        go_up = (pos[0], pos[1] + 1)
        go_down = (pos[0], pos[1] - 1)
        go_left = (pos[0] - 1, pos[1])
        go_right = (pos[0] + 1, pos[1])
        
        neighbours = [go_up, go_down, go_left, go_right]
        neighbours_in_path = 0
        for neighbour in neighbours:
            if neighbour in self.path:
                neighbours_in_path += 1

        if neighbours_in_path > 1:
            return False

        is_up_first = random() < 0.65
        if is_up_first:
            neighbours = [go_right, go_down]
            shuffle(neighbours)
            neighbours = [go_up] + neighbours
        else:
            neighbours = [go_right, go_down]
            shuffle(neighbours)
            neighbours = neighbours + [go_up]
        
        self.path.append(pos)

        for neighbour in neighbours:
            if self.__generate_path(neighbour):
                return True
            
        self.path.remove(pos)
        return False

    def __generate_obstacles(self) -> None:
        def near_path(pos: tuple[int, int]) -> bool:
            return any([abs(pos[0] - x) <= 1 and abs(pos[1] - y) <= 1 for x, y in self.path])


        not_path = [(x, y) for x in range(MAP_SIZE_X) 
                    for y in range(MAP_SIZE_Y) 
                    if not near_path((x, y))]
        
        while len(self.obstacles) < OBSTACLES_AMOUNT:
            self.obstacles.spawn(choice(not_path))
            not_path.remove(self.obstacles[-1])

    def __generate_map(self) -> None:
        self.__generate_path(self._start)
        self.__generate_obstacles()


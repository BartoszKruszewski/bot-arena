from random import choice
from ..stats import MAP_SIZE_X, MAP_SIZE_Y, OBSTACLES_AMOUNT

class Map():
    def __init__(self) -> None:
        self._start = (0, 0)
        self._end = (MAP_SIZE_X - 1, MAP_SIZE_Y - 1)

        self.path = [self._start]
        self.obstacles = []
        self.__generate_map()

        self.MAP_SIZE_X = MAP_SIZE_X
        self.MAP_SIZE_Y = MAP_SIZE_Y

    def __generate_path(self) -> None:
        path = [self._start]

        while path[-1] != self._end:
            next = path[-1]
            where = choice(((0, 1), (1, 0)))
            next = (next[0] + where[0], next[1] + where[1])

            if next[0] < MAP_SIZE_X and next[1] < MAP_SIZE_Y:
                path.append(next)

        self.path = path

    def __generate_obstacles(self) -> None:
        def near_path(pos: tuple[int, int]) -> bool:
            return any([abs(pos[0] - x) <= 1 and abs(pos[1] - y) <= 1 for x, y in self.path])


        not_path = [(x, y) for x in range(MAP_SIZE_X) 
                    for y in range(MAP_SIZE_Y) 
                    if not near_path((x, y))]
        
        while len(self.obstacles) < OBSTACLES_AMOUNT:
            self.obstacles.append(choice(not_path))
            not_path.remove(self.obstacles[-1])

    def __generate_map(self) -> None:
        self.__generate_path()
        self.__generate_obstacles()


from random import shuffle
from ..stats import MAP_SIZE_X, MAP_SIZE_Y, OBSTACLES_AMOUNT
from random import choice

class Map():
    def __init__(self) -> None:
        self._start = (0, 0)
        self._end = (MAP_SIZE_X - 1, MAP_SIZE_Y - 1)

        self.path = []
        self.obstacles = []
        self.__generate_map()

        self.MAP_SIZE_X = MAP_SIZE_X
        self.MAP_SIZE_Y = MAP_SIZE_Y



    def __generate_path(self, pos) -> None:
        # generate path without loops using backtracking
        if pos in self.path:
            return False
        if pos == self._end:
            return True
        
        if pos[0] < 0 or pos[0] >= MAP_SIZE_X or pos[1] < 0 or pos[1] >= MAP_SIZE_Y:
            return False
        
        neighbours = [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1]), (pos[0], pos[1] - 1)]
    
        neighbours_in_path = 0
        for neighbour in neighbours:
            if neighbour in self.path:
                neighbours_in_path += 1

        if neighbours_in_path > 1:
            return False
        
        # Path can't go left
        neighbours.remove(neighbours[2])
        shuffle(neighbours)

        self.path.append(pos)

        for neighbour in neighbours:
            if self.__generate_path(neighbour):
                return True
            
        self.path.remove(pos)
        return False
        

         

    def __generate_path_old(self) -> None:
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
        self.__generate_path(self._start)
        self.__generate_obstacles()


from .stats import MAP_SIZE_X, MAP_SIZE_Y, OBSTACLES_AMOUNT, START_RESOURCES, COST
from random import choice

class Map():
    def __init__(self) -> None:
        self._start = (0, 0)
        self._end = (MAP_SIZE_X - 1, MAP_SIZE_Y - 1)

        self.path = [self._start]
        self.obstacles = []
        self.__generate_map()

        self.MAP_SIZE_X = MAP_SIZE_X
        self.MAP_SIZE_Y = MAP_SIZE_Y

        # turret: list of cords
        self.structures = {side: {         
            "turret":       [],                             
        } for side in ("left", "right")
        }

        # path index: hp
        self.soldiers = {side: {
            cord: None for cord in range(-1, len(self.path)+2)
            } for side in ("left", "right")
        }

        self.stats = {side: {
                'gold': START_RESOURCES['gold'],
            } for side in ('left', 'right')
        }


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
        not_path = [(x, y) for x in range(MAP_SIZE_X) 
                    for y in range(MAP_SIZE_Y) 
                    if (x, y) not in self.path]
        
        while len(self.obstacles) < OBSTACLES_AMOUNT:
            self.obstacles.append(choice(not_path))
            not_path.remove(self.obstacles[-1])

    def __generate_map(self) -> None:
        self.__generate_path()
        self.__generate_obstacles()

    def _print_map(self) -> None:
        soldiers_left = [s for s in range(len(self.path)) if self.soldiers['left'][s] is not None]
        soldiers_right = [s for s in range(len(self.path)) if self.soldiers['right'][s] is not None]

        soldiers_life_left = [self.soldiers['left'][s] for s in soldiers_left]
        soldiers_life_right = [self.soldiers['right'][s] for s in soldiers_right]

        soldiers_left = [self.path[s] for s in soldiers_left]
        soldiers_right = [self.path[s] for s in soldiers_right]


        for y in range(MAP_SIZE_Y):
            for x in range(MAP_SIZE_X):
                if (x, y) in self.path:
                    if (x, y) in soldiers_left:
                        print(soldiers_life_left[soldiers_left.index((x, y))], end='')
                    elif (x, y) in soldiers_right:
                        print(soldiers_life_right[soldiers_right.index((x, y))], end='')
                    else:
                        print('.', end='')
                elif (x, y) in self.structures['left']['turret']:
                    print('l', end='')
                elif (x, y) in self.structures['right']['turret']:
                    print('r', end='')
                else:
                    print(' ', end='')
            print()
            

if __name__ == "__main__":
    m = Map()
    m._print_map()
    print(len(m.obstacles))


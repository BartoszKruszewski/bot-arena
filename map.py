from const import MAP_SIZE, MAP_SIZE_X, MAP_SIZE_Y, TREES_AMOUNT
from random import choice
from pygame import Vector2

placable_ids = ('spawn', 'turret', 'farm')


def are_in_board(cords: Vector2) -> bool:
    '''Returns True if cords are in board.
    '''
    if cords.x < 0 or cords.y < 0:
        return False
    if cords.x >= MAP_SIZE_X or cords.y >= MAP_SIZE_Y:
        return False
    return True


class Map():
    def __init__(self) -> None:
        self.start = Vector2(0, 0)
        self.end = Vector2(MAP_SIZE_X - 1, MAP_SIZE_Y - 1)

        self.structures = {
            "spawn":  [],           # spawn
            "turret": [],           # turret
            "farm":   [],           # farm
            "path":   [self.start], # path
            "trees":  []            # trees
        }

    def can_be_placed(self, cords: Vector2, structure_id: str) -> bool:
        '''Returns True if in cords structure can be placed.
        '''

        if not are_in_board(cords):
            return False

        if any(cords in structure_list for structure_list in self.structures.values()):
            return False

        if structure_id not in placable_ids:
            return False

        return True

    def place_structure(self, cords: Vector2, structure_id: str) -> bool:
        '''Place structure in cords.

        Return True if operation was successful.
        '''
        if not self.can_be_placed(cords, structure_id):
            return False

        self.structures[structure_id].append(cords)
        return True

    def print_path(self) -> None:
        '''Print path to the console.
        '''
        map = [["_" for i in range(MAP_SIZE_X)] for j in range(MAP_SIZE_Y)]

        for key, items in self.structures.items():
            for pos in items:
                map[pos.y][pos.x] = key
                if key == "path":
                    map[pos.y][pos.x] = "#"

        for row in map:
            print(" ".join(row))

    def load_map(self, path: str) -> None:
        '''Loads path from file.
        '''
        # TODO: load path from file
        pass

    def generate_map(self) -> None:
        '''Generate random path.
        '''

        # TODO: generate from seed
        # TODO: make better generator
        # TODO: genereate trees and grass

        path = [self.start]
        while path[-1] != self.end:
            next = list(path[-1])
            where = choice((Vector2(0, 1), Vector2(1, 0)))
            next += where

            if next.x < MAP_SIZE_X and next.y < MAP_SIZE_Y:
                path.append(next)

        grass = []
        for y in range(MAP_SIZE_Y):
            for x in range(MAP_SIZE_X):
                tile = Vector2(x, y)
                if tile not in path:
                    grass.append(tile)

        trees = []
        good_places = []
        
        for v in grass:
            surr = [Vector2(v.x + x, v.y + y) for x in range(-1, 2) for y in range(-1, 2)]
            good = True
            for u in surr:
                if u in path:
                    good = False
                    break
            if good:    
                good_places.append(v)


        for _ in range(TREES_AMOUNT):
            tile = choice(good_places)
            trees.append(tile)
            grass.remove(tile)
            good_places.remove(tile)

        self.structures["path"] = path
        self.structures["trees"] = trees

if __name__ == "__main__":
    map = Map()
    map.generate_map()
    map.print_path()

    print()

    map.place_structure((0, 5), "spawn")
    map.place_structure((-1, 0), "tree")
    map.place_structure((3, 3), "tree")
    map.print_path()

from const import MAP_SIZE, MAP_SIZE_X, MAP_SIZE_Y
from random import choice
from pygame import Vector2

placable_ids = ("S", "T", "F")


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
            "S": [],            # spawn
            "T": [],            # turret
            "F": [],            # farm
            "P": [self.start]   # path
        }

    def can_be_placed(self, cords: Vector2, structure_id: str) -> bool:
        '''Returns True if in cords structure can be placed.
        '''
        if type(cords) != tuple:
            raise Exception

        if not are_in_board(cords):
            return False

        if cords in sum(self.structures.items()):
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
                if key == "P":
                    map[pos.y][pos.x] = "#"

        for row in map:
            print(" ".join(row))

    def load_path(self, path: str) -> None:
        '''Loads path from file.
        '''
        # TODO: load path from file
        pass

    def generate_path(self) -> None:
        '''Generate random path.
        '''
        # TODO: generate from seed
        # TODO: make better generator
        path = [self.start]
        while path[-1] != self.end:
            next = list(path[-1])
            where = choice(Vector2(0, 1), Vector2(1, 0))
            next += where

            if next.x < MAP_SIZE_X and next.y < MAP_SIZE_Y:
                path.append(next)

        self.structures["P"] = path

    def get_struct(self, structure_id: str) -> str:
        '''Gets full name of structure with structure_id.
        '''
        TILE_TYPES = {
            'S': 'spawn',
            'T': 'turret',
            'F': 'farm',
            'P': 'path',
        }
        if structure_id not in TILE_TYPES.keys():
            return None
        
        return TILE_TYPES[structure_id]

if __name__ == "__main__":
    map = Map()
    map.generate_path()
    map.print_path()

    print()

    map.place_structure((0, 5), "S")
    map.place_structure((-1, 0), "T")
    map.place_structure((3, 3), "T")
    map.print_path()

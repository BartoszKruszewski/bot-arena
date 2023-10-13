from const import MAP_SiZE
from random import choice

placable_ids = ("S", "T", "F")


def are_in_board(cords) -> bool:
    if cords[0] < 0 or cords[1] < 0:
        return False
    if cords[0] >= MAP_SiZE or cords[1] >= MAP_SiZE:
        return False
    return True


class Map():
    def __init__(self) -> None:
        self.start = (0, 0)
        self.end = (MAP_SiZE - 1, MAP_SiZE - 1)

        self.structures = {
            "S": [],            # spawn
            "T": [],            # turret
            "F": [],            # farm
            "P": [self.start]   # path
        }

    def can_be_placed(self, cords, structure_id) -> bool:
        if type(cords) != tuple:
            raise Exception

        if not are_in_board(cords):
            return False

        if cords in self.structures.items():
            return False

        if structure_id not in placable_ids:
            return False

        return True

    def place_structure(self, cords, structure_id) -> bool:
        if not self.can_be_placed(cords, structure_id):
            return False

        self.structures[structure_id].append(cords)
        return True

    def print_path(self) -> None:
        map = [["_" for i in range(MAP_SiZE)] for j in range(MAP_SiZE)]

        for key, items in self.structures.items():
            for x, y in items:
                map[x][y] = key
                if key == "P":
                    map[x][y] = "#"

        for row in map:
            print(" ".join(row))

    def load_path(self, path) -> None:
        # TODO: load path from file
        pass

    def generate_path(self) -> None:
        # TODO: generate from seed
        # TODO: make better generator
        path = [self.start]
        while path[-1] != self.end:
            next = list(path[-1])
            where = choice([[0, 1], [1, 0]])
            next[0] += where[0]
            next[1] += where[1]
            next = tuple(next)

            if next[0] < MAP_SiZE and next[1] < MAP_SiZE:
                path.append(next)

        self.structures["P"] = path


if __name__ == "__main__":
    map = Map()
    map.generate_path()
    map.print_path()

    print()

    map.place_structure((0, 5), "S")
    map.place_structure((-1, 0), "T")
    map.place_structure((3, 3), "T")
    map.print_path()

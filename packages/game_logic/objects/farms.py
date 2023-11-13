class Farm():
    def __init__(self, cords, id) -> None:
        self.cords = cords
        self.id = id

class Farms():
    def __init__(self, path) -> None:
        self.farms = []
        self.next_id = 0
        self.path = path

    def spawn(self, cords: tuple[int, int]) -> None:
        self.farms.append(Farm(cords, id=self.next_id))
        self.next_id += 1

    def __iter__(self) -> iter:
        for turret in self.farms:
            yield turret.cords

    def __len__(self) -> int:
        return len(self.farms)
        
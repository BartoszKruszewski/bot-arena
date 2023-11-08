from .soldiers import Soldiers

class Turret():
    def __init__(self, cords, id) -> None:
        self.cords = cords
        self.attack = 10
        self.id = id
        self.range = 5

    def _is_in_range(self, cords: tuple[int, int]) -> bool:
        return abs(self.cords[0] - cords[0]) + abs(self.cords[1] - cords[1]) <= self.range

    def _shoot(self, soldiers: Soldiers, path: list[tuple]) -> None:
        for soldier in soldiers.soldiers:
            if self._is_in_range(path[soldier.position]):
                soldier.hp -= self.attack
                break

class Turrets():
    def __init__(self, path) -> None:
        self.turrets = []
        self.next_id = 0
        self.path = path

    def spawn(self, cords: tuple[int, int]) -> None:
        self.turrets.append(Turret(cords, id=self.next_id))
        self.next_id += 1

    def shoot(self, soldiers: Soldiers) -> None:
        for turret in self.turrets:
            turret._shoot(soldiers, self.path)

    def __iter__(self) -> iter:
        for turret in self.turrets:
            yield turret.cords
        
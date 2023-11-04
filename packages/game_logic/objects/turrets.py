from .soldiers import Soldiers

class _Turret():
    def __init__(self) -> None:
        pass

class Turrets():
    def __init__(self) -> None:
        self.turrets = []

    def spawn(self, cords: tuple[int, int]) -> None:
        self.turrets.append(cords)
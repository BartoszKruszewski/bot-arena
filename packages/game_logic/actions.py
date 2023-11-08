class Action():
    def __init__(self, side) -> None:
        self.side = side

class Wait(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

class BuildTurret(Action):
    def __init__(self, side, x, y) -> None:
        super().__init__(side)
        x, y = int(x), int(y)
        self.cords = (x, y)

class SpawnSoldier(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

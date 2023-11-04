class Action():
    def __init__(self, side) -> None:
        self.side = side

class Wait(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

class BuildTurret(Action):
    def __init__(self, side, cords) -> None:
        super().__init__(side)
        self.cords = cords

class SpawnSoldier(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

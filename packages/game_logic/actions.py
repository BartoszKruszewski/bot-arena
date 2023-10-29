class Action():
    def __init__(self, side) -> None:
        self.player = side

class Wait(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

class BuildTurret(Action):
    def __init__(self, side, cord) -> None:
        super().__init__(side)
        self.cord = cord

class SpawnSoldier(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

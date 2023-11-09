__all__ = ['Wait', 'BuildTurret', 'BuildFarm', 'SpawnSoldier']

class Action():
    def __init__(self, side) -> None:
        self.side = side

class BuildAction(Action):
    def __init__(self, side, x, y) -> None:
        super().__init__(side)
        x, y = int(x), int(y)
        self.cords = (x, y)

class Wait(Action):
    def __init__(self, side) -> None:
        super().__init__(side)

class BuildTurret(BuildAction):
    def __init__(self, side, x, y) -> None:
        super().__init__(side, x, y)

class BuildFarm(BuildAction):
    def __init__(self, side, x, y) -> None:
        super().__init__(side, x, y)

class SpawnSoldier(Action):
    def __init__(self, side, name) -> None:
        super().__init__(side)
        self.name = name





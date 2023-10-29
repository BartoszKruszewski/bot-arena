class Action():
    def __init__(self, time, player) -> None:
        self.time = time
        self.player = player

class Wait(Action):
    def __init__(self, time, player) -> None:
        super().__init__(time, player)

class BuildTurret(Action):
    def __init__(self, time, player, cord) -> None:
        super().__init__(time, player)
        self.cord = cord

class SpawnSoldier(Action):
    def __init__(self, time, player) -> None:
        super().__init__(time, player)

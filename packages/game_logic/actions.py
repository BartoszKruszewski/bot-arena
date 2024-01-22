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
    
    def __str__(self) -> str:
        return "W"

class BuildTurret(BuildAction):
    def __init__(self, side, x, y) -> None:
        super().__init__(side, x, y)

    def __str__(self) -> str:
        return f"T {self.cords[0]} {self.cords[1]}"

class BuildFarm(BuildAction):
    def __init__(self, side, x, y) -> None:
        super().__init__(side, x, y)

    def __str__(self) -> str:
        return f"F {self.cords[0]} {self.cords[1]}"

class SpawnSoldier(Action):
    def __init__(self, side, name) -> None:
        super().__init__(side)
        self.name = name

    def __str__(self) -> str:
        return f"S {self.name}"
    
__letter_to_action = {
    'W': Wait,
    'S': SpawnSoldier,
    'T': BuildTurret,
    'F': BuildFarm
}

def str_to_actions(string):
    if type(string) == str:
        string = string.split(" ")

    left_side, right_side = string[:string.index("|")], string[string.index("|")+1:]
    left_action, right_action = left_side[0], right_side[0]
    left_args, right_args = ["left"] + left_side[1:], ["right"] + right_side[1:]
    
    left_action = __letter_to_action[left_action[0]]
    right_action = __letter_to_action[right_action[0]]
                                                   
    left_action = left_action(*left_args)
    right_action = right_action(*right_args)

    return left_action, right_action

def str_to_action(string, side):
    if type(string) == str:
        string = string.split(" ")

    action = string[0]
    args = [side] + string[1:]

    action = __letter_to_action[action[0]]
    action = action(*args)

    return action





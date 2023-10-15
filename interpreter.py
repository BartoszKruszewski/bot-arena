class Interpreter():
    def __init__(self):
        pass

    def get_action(self, input):
        return Action('none', 0, 'left')

class Action():
    def __init__(self, name, value, side) -> None:
        self.name = name
        self.value = value
        self.side = side

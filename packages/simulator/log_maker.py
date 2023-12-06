from packages import LOGS_DIRECTORY

class LogMaker():
    def __init__(self, name):
        self.name = name
        self.path = LOGS_DIRECTORY + "/" + name + ".txt"

        self.actions = []

    def add_actions(self, action1, action2):
        self.actions.append(" | ".join([action1, action2]))

    def save(self):
        with open(self.path, "w") as file:
            file.write("\n".join(self.actions))


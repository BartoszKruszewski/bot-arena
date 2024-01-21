from packages import LOGS_DIRECTORY
import os

class LogMaker():
    def __init__(self, name, number):
        self.name = name
        os.makedirs(os.path.join(LOGS_DIRECTORY, name), exist_ok=True)
        self.path = os.path.join(LOGS_DIRECTORY, name, number)

        self.actions = []

    def add_actions(self, action1, action2):
        self.actions.append(" | ".join([action1, action2]))

    def save(self, winner, 
             map_name,
             player1_name,
             player2_name):
        self.path = self.path + f"_{player1_name}_{player2_name}_{winner}.log"
        with open(self.path, "w") as file:
            file.write("map:" + map_name + "\n")
            file.write("player1:" + player1_name + "\n")
            file.write("player2:" + player2_name + "\n")
            file.write("\n".join(self.actions))

    def clear(log_name):
        try:
            path = os.path.join(LOGS_DIRECTORY, log_name)
            for file in os.listdir(path):
                os.remove(os.path.join(path, file))
        except FileNotFoundError:
            pass

        
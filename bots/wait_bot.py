import os
import json

class BOT():
    def __init__(self): 
        game_timeout, move_timeout, ready_timeout, side = input().split()
        self.game_timeout = game_timeout
        self.move_timeout = move_timeout
        self.ready_timeout = ready_timeout
        self.side = side

        map_name = input()
        map = os.path.dirname(__file__)
        map = os.path.dirname(map)
        map = os.path.join(map, "maps", map_name)
        map = json.load(open(map, "r"))
        self.map = map

        self.preprocess()

        print("READY")

        while True:
            move = self.make_move()
            print(move)
            message = input()

            if message == "END":
                break

            self.update(message)

    # user defined functions  
    def preprocess(self):
        pass

    def update(self, message):
        pass

    def make_move(self):
        return "W"

while True:
    BOT()
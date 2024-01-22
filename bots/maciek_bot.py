import random
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from packages.game_logic.actions import str_to_actions, str_to_action, Wait
from packages.game_logic.game import Game, ErrorCode

DEPTH = 1

class BOT():
    def __init__(self): 
        game_timeout, move_timeout, ready_timeout, side = input().split()
        self.game_timeout = game_timeout
        self.move_timeout = move_timeout
        self.ready_timeout = ready_timeout
        self.side = side

        self.map_name = input()
        map = os.path.dirname(__file__)
        map = os.path.dirname(map)
        map = os.path.join(map, "maps", self.map_name)
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
        # setup game
        self.game = Game(self.map_name)
        map_x = self.map["MAP_SIZE_X"]
        map_y = self.map["MAP_SIZE_Y"]
        my_base = (0, 0) if self.side == "left" else (map_x - 1, map_y - 1)
        all_cords = [(x, y) for x in range(map_x) for y in range(map_y)]
        self.path = self.map.get("path", [])
        self.obstacles = self.map.get("obstacles", [])
        all_cords = list(filter(lambda x: x not in self.path and x not in self.obstacles, all_cords))
        
        def near_path(cords):
            for x, y in self.path:
                if abs(x - cords[0]) + abs(y - cords[1]) <= 3:
                    return True
            return False
        
        self.tower_cords = list(filter(near_path, all_cords))
        self.farm_cords = list(filter(lambda x: not near_path(x), all_cords))
        self.tower_cords.sort(key=lambda x: abs(x[0] - my_base[0]) + abs(x[1] - my_base[1]))


    def update(self, message):
        left_action, right_action = str_to_actions(message)
        self.game.update(left_action, right_action)

    def make_move(self):
        enemy_soldiers = self.game.get_soldiers()["left" if self.side == "right" else "right"] 
        my_soldiers = self.game.get_soldiers()[self.side]

        MY_BASE = 1 if self.side == 'left' else len(self.path) - 2
        if any(soldier.position == MY_BASE for soldier in enemy_soldiers):
            if len(my_soldiers) == 0:
                return "S swordsman"
            
        if len(self.tower_cords) > 0:
            x, y = self.tower_cords[0]
            self.tower_cords = self.tower_cords[1:]
            return f"T {x} {y}"

        if len(self.farm_cords) > 0:
            x, y = self.farm_cords[0]
            self.farm_cords = self.farm_cords[1:]
            return f"F {x} {y}"

        return "S swordsman"            
        
        
    
        

            
                

            


while True:
    BOT()
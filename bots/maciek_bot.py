import random
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bot_package.bot import Bot
from bot_package.move import Move

class Maciek_Bot(Bot):
    def preprocess(self):
        # setup game
        map = self.arena_properties["arena"]

        self.map_size = map["map_size"]
        self.my_base = map["base"][self.side]
        self.path = map["path"]
        self.obstacles = map["obstacles"]

        all_cords = [(x, y) for x in range(self.map_size[0]) for y in range(self.map_size[1])]
        all_cords = list(filter(lambda x: x not in self.path and x not in self.obstacles, all_cords))

        def near_path(cords):
            for x, y in self.path:
                if abs(x - cords[0]) + abs(y - cords[1]) <= 3:
                    return True
            return False
        
        self.tower_cords = list(filter(near_path, all_cords))
        self.farm_cords = list(filter(lambda x: not near_path(x), all_cords))
        self.tower_cords.sort(key=lambda x: abs(x[0] - self.my_base[0]) + abs(x[1] - self.my_base[1]))

        self.post_move_action()

        
    def post_move_action(self) -> None:
        self.enemy_soldiers = self.arena_properties["players"]["left" if self.side == "right" else "right"]["units"]
        self.my_soldiers = self.arena_properties["players"][self.side]["units"]

        self.my_gold = self.arena_properties["players"][self.side]["gold"]

    def make_move(self):

        MY_BASE = 2 if self.side == 'left' else len(self.path) - 3
        if any(soldier_position == MY_BASE for soldier_position in self.enemy_soldiers):
            if len(self.my_soldiers) < 3:
                return Move.Spawn("swordsman")
            
        if self.my_gold <= 250:
            return Move.Wait()

        if len(self.farm_cords) > 0:
            x, y = self.farm_cords[0]
            self.farm_cords = self.farm_cords[1:]
            return Move.Build.Farm(x, y)
    
        if len(self.tower_cords) > 0:
            x, y = self.tower_cords[0]
            self.tower_cords = self.tower_cords[1:]
            return Move.Build.Turret(x, y)


        return Move.Spawn("swordsman")          
        
        
while True:
    Maciek_Bot().run()
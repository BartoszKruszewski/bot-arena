import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bot_package.bot import Bot
from bot_package.move import Move

class Random_Bot(Bot):
    def preprocess(self) -> None:
        self.map_size = self.arena_properties["arena"]["map_size"]

    def make_move(self):
        x = random.randint(0, self.map_size[0] - 1)
        y = random.randint(0, self.map_size[1] - 1)

        move = random.choice(['W', 'T', 'F', 'S'])
        import sys 
        print("RAND", file=sys.stderr)
        if move == 'W':
            return Move.Wait()
        elif move == 'T':
            return Move.Build.Turret(x, y)
        elif move == 'F':
            return Move.Build.Farm(x, y)
        elif move == 'S':
            return Move.Spawn(unit_type= random.choice(["swordsman", "archer"]))
        else:
            return f'W'

while True:
    Random_Bot().run()
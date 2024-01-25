import random

from bot_package.bot import Bot
from bot_package.move import Move

class Wait_bot(Bot):
    
    def make_move(self):
        import sys
        import sys
        print("SPAWN", file=sys.stderr)
        return Move.Spawn(unit_type= random.choice(["swordsman", "archer"]))

while True:
    Wait_bot.run()
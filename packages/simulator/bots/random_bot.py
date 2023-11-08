#!/usr/bin/env python3

import random
import sys
class RandomBot:
    def __init__(self):
        test = None
    def run(self):
        while True:
            input = sys.stdin
            if not input:
                break

            move = random.choice(["rock", "paper", "scissors"])

            print(move)
            sys.stdout.flush()



bot = RandomBot()
bot.run()

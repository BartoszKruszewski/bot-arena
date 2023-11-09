#!/usr/bin/env python3

import random
import json
import sys

class Bot:
    def __init__(self):
        self.game_data = {}

    def handle_request(self, method, data=None):
        if method == 'GET':
            move = self.random_move()
            return move
        elif method == 'POST':
            if data:
                self.game_data = self.process_data(data)
            return 'S'
        else:
            return "Unsupported method"

    def process_data(self, data):
        try:
            data_dict = json.loads(data)
            return data_dict
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            return None

    def run(self):
        while True:
            line = sys.stdin.readline().strip()
            if line == '':
                break
            method = line.strip()

            if method in ['GET', 'POST']:
                if method == 'POST':
                    data = sys.stdin.readline().strip()
                else:
                    data = None
                response = self.handle_request(method, data)
                print(response)

    def random_move(self):
        move = random.choice(self.valid_moves)
        if move == 'T':
            maxX = self.game_data['arena']['map_size'][0]
            maxY = self.game_data['arena']['map_size'][1]

            x = random.randint(0, maxX)
            y = random.randint(0, maxY)
            return f'T {x} {y}'
        return move

bot = Bot()
bot.run()
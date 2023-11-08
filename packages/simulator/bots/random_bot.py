#!/usr/bin/env python3

import random
import json


class RandomBot:
    def __init__(self):
        self.valid_moves = ['W', 'A', 'S', 'D']
        self.game_data = {}

    def random_move(self):
        return random.choice(self.valid_moves)

    def handle_request(self):
        input_data = input()
        request = json.loads(input_data)

        if 'GET' in request:
            self.handle_get_request(request['GET'])
        else:
            response = json.dumps({'error': 'invalid request'})
            print(response)

    def handle_get_request(self, request: dict):
        if 'move' in request:
            move = self.random_move()
            response = json.dumps({'move': move})
            print(response)
        else:
            response = json.dumps({'error': f'Invalid get request: missing "move" key'})
            print(response)

    def run(self):
        while True:
            self.handle_request()


if __name__ == "__main__":
    bot = RandomBot()
    bot.run()

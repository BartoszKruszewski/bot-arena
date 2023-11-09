#!/usr/bin/env python3

import random
import json
import sys

class RandomBot:
    def __init__(self):
        self.valid_moves = ['W', 'S', 'T']
        self.game_data = {}


    def handle_request(self):
        request = sys.stdin.readline()

        if 'GET' in request:
            requestJson = json.loads(request)
            self.handle_get_request(requestJson['GET'])
        elif 'POST' in request:
            requestJson = json.loads(request)
            self.handle_post_request(requestJson['POST'])

    def handle_get_request(self, request: str):
        if 'move' == request:
            move = self.random_move()
            response = json.dumps({'move': move})
            print(response)
        else:
            print({'error': f'Invalid get request: missing "game_data" key'})

    def handle_post_request(self, request: dict):
        if 'game_data' in request:
            self.game_data = request['game_data']
        else:
            print({'error': f'Invalid get request: missing "game_data" key'})


    def run(self):
        while True:
            self.handle_request()

    def random_move(self):
        return random.choice(self.valid_moves)

bot = RandomBot()
bot.run()

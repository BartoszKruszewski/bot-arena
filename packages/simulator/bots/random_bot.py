#!/usr/bin/env python3

import random
import json
import sys

class RandomBot:
    def __init__(self):
        self.valid_moves = ['W', 'S', 'T']
        self.game_data = {}

    def handle_request(self):
        while True:
            request = sys.stdin.readline()
            if not request:
                break

            request_data = json.loads(request)
            if 'GET' in request_data:
                self.handle_get_request(request_data['GET'])
            elif 'POST' in request_data:
                self.handle_post_request(request_data['POST'])


    def handle_get_request(self, request: str):
        if 'move' == request:
            move = self.random_move()
            response = json.dumps({'move': move})
            print(response+"\n")
            sys.stdout.flush()
        if 'game_data' in request:
            response = json.dumps({'game_data': self.game_data})
            i
            print(response + "\n")
            sys.stdout.flush()
        else:
            print({'error': f'Invalid get request: missing "move" or "game_data" key'})

    def handle_post_request(self, request: dict):
        if 'game_data' in request:
            self.game_data = json.loads(request)['game_data']
        else:
            print({'error': f'Invalid get request: missing "game_data" key'})


    def random_move(self):
        move = random.choice(self.valid_moves)
        if move == 'T':
            maxX = self.game_data['arena']['map_size'][0]
            maxY = self.game_data['arena']['map_size'][1]

            x = random.randint(0, maxX)
            y = random.randint(0, maxY)
            return f'T {x} {y}'
        return move

bot = RandomBot()
bot.handle_request()

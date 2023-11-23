#!/usr/bin/env python3

import random
import json
import sys

class Bot:
    def __init__(self):
        self.game_data = {}

    def handle_request(self, method, data=None):
        if method == 'GET':
            move = 'W'
            return move
        elif method == 'POST':
            if data:
                self.game_data = self.process_data(data)
            move = 'W'
            return move
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
                sys.stdout.flush()


bot = Bot()
bot.run()
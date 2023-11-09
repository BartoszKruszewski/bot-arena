import json
import os

from packages.game_logic.actions import *
from packages.simulator.bot_pipe import BotPipe
from packages.game_logic.game import Game
from packages.simulator.serializer import Serializer

valid_moves = ['S', 'T', 'W', 's', 'w', 't']

class Log:
    def __init__(self):
        self.log_file_name = 'game_log.txt'

        if os.path.exists(self.log_file_name):
            base_name, ext = os.path.splitext(self.log_file_name)
            i = 1
            while os.path.exists(self.log_file_name):
                self.log_file_name = f"{base_name}_{i}{ext}"
                i += 1

        self.log_file = None

    def open(self):
        self.log_file = open(self.log_file_name, 'a')

    def close(self):
        self.log_file.close()
        self.log_file = None

    def update(self, message):
        try:
            if self.log_file is not None:
                self.log_file.write(message + '\n')
                self.log_file.flush()
            else:
                raise ValueError('Log is not open. Please open the log before updating.')
        except ValueError as e:
            print(e)
class GameController:

    def __init__(self, bot_left: str, bot_right: str):
        self.bot_left = BotPipe(bot_left)
        self.bot_right = BotPipe(bot_right)

        self.game = Game()
        self.log = Log()

    def run(self):
        game_over = False
        self.log.open()

        while not game_over:
            self.post_game_data(self.bot_left)
            self.post_game_data(self.bot_right)


            right_command = self.get_command(self.bot_right)
            left_command = self.get_command(self.bot_left)

            self.log.update(left_command.upper() + '|' + right_command.upper())

            left_action = self.command_to_action(left_command,'left')
            right_action = self.command_to_action(right_command, 'right')

            self.game.update(left_action, right_action)

        self.log.close()

    def command_to_action(self, move: str, side: str):
        if side not in ['left', 'right']:
            raise ValueError("Invalid side, please use 'left' or 'right'.")

        move = move.upper()

        if move == 'W':
            return Wait(side)
        elif move == 'S':
            return SpawnSoldier(side)
        elif move[0] == 'T':
            move = move.split(' ')
            x = int(move[1])
            y = int(move[2])
            return BuildTurret(side, x, y)
        else:
            print("Wrong command")
            return Wait(side)

    def get_command(self, bot: BotPipe) -> str:
        responseJson = bot.GET('move')
        print(json.loads(responseJson))
        response = None

        if responseJson is not None:
            response = json.loads(responseJson)

        while 'error' in response:
            responseJson = bot.GET('move')
            print(responseJson)

            if responseJson is not None:
                response = json.loads(responseJson)

        return response['move']

    def post_game_data(self, bot:BotPipe):
        game_data = json.dumps({'game_data': Serializer.get(self.game)})
        bot.POST(game_data)





if __name__ == '__main__':
    game = GameController('./bots/random_bot.py','./bots/random_bot.py')
    game.run()



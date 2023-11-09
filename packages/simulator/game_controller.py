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
            game_dataJson = json.dumps(Serializer.get(self.game))
            response_left = self.bot_left.request(method='POST', data= game_dataJson)
            response_right = self.bot_right.request(method='POST',data= game_dataJson)

            self.log.update(response_left + ' | ' + response_right)

            left_action = self.command_to_action(response_left,'left')
            right_action = self.command_to_action(response_right, 'right')

            game_status = self.game.update(left_action, right_action)
            game_over = self.is_game_over(game_status)

        self.log.close()

    def is_game_over(self, game_status: tuple[str, str]):
        if game_status[0] in ['Left win', 'Right win', 'Tie']:
            return True
        else:
            return False

    def command_to_action(self, move: str, side: str):
        if side not in ['left', 'right']:
            raise ValueError("Invalid side, please use 'left' or 'right'.")

        move = move.upper()
        print(move)

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


if __name__ == '__main__':
    game = GameController('./bots/random_bot.py','./bots/random_bot.py')
    game.run()



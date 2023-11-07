from packages.game_logic.game import Game
from packages.game_logic.actions import *
from packages.simulator.api_handler import *
from packages.simulator.bots.random_bot import RandomBot

import time
import os
import threading
import logging

# Set the logging level to suppress unnecessary output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def bot_thread_function():
    bot = RandomBot("http://127.0.0.1:5000")
    bot.run()

def api_handler_thread_function(api_handler):
    api_handler.app.run()

def run():
    game = Game()
    api_handler = ApiHandler(game)

    # Start the API handler process
    api_handler_thread = threading.Thread(target=api_handler_thread_function, args=(api_handler,))
    api_handler_thread.start()

    # Start the bot process
    bot_thread = threading.Thread(target=bot_thread_function)
    bot_thread.start()

    # Game simulation
    os.system('cls')

    action_left = None
    action_right = None

    while True:
        time.sleep(5)
        command = api_handler._last_command

        if command == 'w':
            action_left = Wait('left')
            action_right = Wait('right')
        elif command == 'l':
            action_left = SpawnSoldier('left')
        elif command == 'r':
            action_right = SpawnSoldier('right')
        elif command == 'b':
            action_left = SpawnSoldier('left')
            action_right = SpawnSoldier('right')
        elif command[0] == 't':
            command = command.split(' ')
            side = command[1]
            x = int(command[2])
            y = int(command[3])
            if side == 'l':
                action_left = BuildTurret('left', (x, y))
            elif side == 'r':
                action_right = BuildTurret('right', (x, y))
        else:
            print("Wrong command")
            continue

        os.system('cls')
        print(command)
        print(game.update(action_left, action_right))
        game._map._print_map()

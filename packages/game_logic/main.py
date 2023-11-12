from packages.game_logic.game import Game
from packages.game_logic.actions import *

def TestRun():
    import os
    game = Game()
    os.system('cls' if os.name == 'nt' else 'clear')
    status = None

    while True:
        command = input('Enter command: ')
        if command == 'l':
            status = game.update(SpawnSoldier('left', 'basic'), Wait('right'))
        elif command == 'r':
            status = game.update(Wait('left'), SpawnSoldier('right', 'basic'))
        elif command == 'lr':
            status = game.update(SpawnSoldier('left', 'basic'), SpawnSoldier('right', 'basic'))
        elif command[0:2] == 'lt':
            command = command.split(' ')
            status = game.update(BuildTurret('left', int(command[1]), int(command[2])), Wait('right'))
        elif command[0:2] == 'rf':
            command = command.split(' ')
            status = game.update(Wait('left'), BuildFarm('right', int(command[1]), int(command[2])))
        elif command[0:2] == 'lf':
            command = command.split(' ')
            status = game.update(BuildFarm('left', int(command[1]), int(command[2])), Wait('right'))
        elif command[0:2] == 'rt':
            command = command.split(' ')
        else:
            status = game.update(Wait('left'), Wait('right'))

        os.system('cls' if os.name == 'nt' else 'clear')
        print(status)
        game.display()

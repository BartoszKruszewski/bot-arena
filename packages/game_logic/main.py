from packages.game_logic.game import Game
from packages.game_logic.actions import *

def TestRun():
    import os
    game = Game()

    status = None

    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print(status)
        game.display()

        command = input('Enter command: ')
        if command == 'l':
            status = game.update(SpawnSoldier('left'), Wait('right'))
        elif command == 'r':
            status = game.update(Wait('left'), SpawnSoldier('right'))
        elif command == 'lr':
            status = game.update(SpawnSoldier('left'), SpawnSoldier('right'))
        elif command[0:2] == 'lt':
            command = command.split(' ')
            status = game.update(BuildTurret('left', (int(command[1]), int(command[2]))), Wait('right'))
        elif command[0:2] == 'rt':
            command = command.split(' ')
            status = game.update(Wait('left'), BuildTurret('right', (int(command[1]), int(command[2]))))
        else:
            status = game.update(Wait('left'), Wait('right'))


        








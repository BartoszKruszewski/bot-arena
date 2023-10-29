from .game import Game
from .actions import *
import os

def test():
    game = Game()

    os.system('cls')

    while(True):
        print("Enter action: ")
        print("l - spawn left soldier")
        print("r - spawn right soldier")
        print("b - spawn left and right soldier")
        print("t [l/r] [x] [y] - build turret")
        print("enter - next turn")
        print("q - quit")

        command = input()
        action_left = Wait('left')
        action_right = Wait('right')
        if command == '':
            pass
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
        elif command == 'q':
            break
        else:
            print("Wrong command")
            continue

        
        os.system('cls')
        print(game.update(action_left, action_right))
        game._map._print_map()


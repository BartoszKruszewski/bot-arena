from .game import Game
from .actions import *

def test():
    game = Game()
    def print_soldiers():
        for i in range(len(game._map.path)):
            if game._map.soldiers['left'][i]:
                print('L', end='')
            elif game._map.soldiers['right'][i]:
                print('R', end='')
            else:
                print('.', end='')
        print()


    while(True):
        is_spawn = input('Spawn? (l/r/b/n) ')
        if is_spawn == 'l':
            print(game.update(SpawnSoldier("left"), Wait("right")))
        elif is_spawn == 'r':
            print(game.update(Wait("left"), SpawnSoldier("right")))
        elif is_spawn == 'b':
            print(game.update(SpawnSoldier("left"), SpawnSoldier("right")))
        else:
            print(game.update(Wait("left"), Wait("right")))

        print_soldiers()


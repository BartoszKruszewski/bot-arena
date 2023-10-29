from .game import Game
from .actions import Action




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

    game._map.soldiers['left'][0] = 100
    game._map.soldiers['left'][7] = 20
    game._map.soldiers['right'][13] = 110

    while(True):
        print_soldiers()
        game.update(Action, Action)
        pause = input()

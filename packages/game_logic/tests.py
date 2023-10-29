from .game import Game
from .actions import Action




def test():
    game = Game()
    def print_soldiers():
        for i in range(len(game._map.path)):
            if game._map.soliders['left'][i]:
                print('L', end='')
            elif game._map.soliders['right'][i]:
                print('R', end='')
            else:
                print('.', end='')
        print()

    game._map.soliders['left'][0] = 100
    game._map.soliders['right'][13] = 110

    while(True):
        print_soldiers()
        game.update(Action, Action)
        pause = input()

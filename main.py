from packages.graphics.main import Main 
from packages.game_logic import example

from packages.game_logic.game import Game

if __name__ == '__main__':
    # Main()
    # example.run()

    game = Game()
    actions = game.get_possible_actions()
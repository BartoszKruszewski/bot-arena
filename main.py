# from packages.graphics.main import Main 
def GameTest():
    from packages.game_logic.game import Game
    from packages.game_logic.actions import Wait, BuildTurret, SpawnSoldier
    game = Game()
    Game.display(game)

    while True:
        action = input('Enter action: ')
        if action == 'l':
            log = game.update(SpawnSoldier('left'), Wait('right'))
        elif action == 'r':
            action = game.update(Wait('left'), SpawnSoldier('right'))
        else:
            action = game.update(Wait('left'), Wait('right'))
        Game.display(game)
        print(action)



if __name__ == '__main__':
    GameTest()
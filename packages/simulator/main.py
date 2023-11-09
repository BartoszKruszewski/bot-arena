from packages.simulator.game_controller import GameController

def TestRun():
    random_bot_path = './bots/random_bot.py'
    spawn_only_bot = './bots/spawn_only_bot.py'
    game = GameController(spawn_only_bot, random_bot_path)
    game.run()

if __name__ == '__main__':
    TestRun()
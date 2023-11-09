from packages.simulator.game_controller import GameController


def TestRun():
    bot_path = './bots/random_bot.py'
    game = GameController(bot_path, bot_path)
    game.run()

TestRun()
import sys
import threading

from packages.game_logic.game import Game
from packages.simulator.api_handler import ApiHandler
from packages.simulator.bots.random_bot import RandomBot
class GameClient:
    def __init__(self):
        bot1 = RandomBot('http://127.0.0.1:5000', side='left')
        bot2 = RandomBot('http://127.0.0.1:5000', side='right')
    def run(game: Game()):
        game = Game()
        api_handler = ApiHandler(game)

        # Start the API handler process
        self._api_handler_thread_function(api_handler)

        self._bot_thread_function(self.bot1)
        self._bot_thread_function(self.bot2)



    def _bot_thread_function(self, bot: RandomBot):
        thread = threading.Thread(target=bot.run)
        thread.start()


    def _api_handler_thread_function(api_handler):
        api_handler_thread = threading.Thread(target=api_handler.app.run())
        api_handler_thread.start()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python your_script.py arg1 arg2")
    else:
        bot1 = sys.argv[1]
        bot2 = sys.argv[2]

        try:
            game_client = GameClient(bot1, bot2)
        except FileNotFoundError:
            print("One or both of the specified bot files do not exist.")

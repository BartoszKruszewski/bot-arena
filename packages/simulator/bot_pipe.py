import subprocess
import json

from .serializer import Serializer
from ..game_logic.game import Game



class BotPipe:
    def __init__(self, bot_path: str):
        self.bot_process = None
        self.bot_in = None
        self.bot_out = None

        try:
            self.bot_process = subprocess.Popen(
                'python3 '+bot_path,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                text=True
            )

            self.bot_in = self.bot_process.stdin
            self.bot_out = self.bot_process.stdout

        except FileNotFoundError as e:
            print(f"Bot file not found: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def request(self, method, data=None):
        if method == 'GET':
            self.bot_process.stdin.write('GET\n')
            self.bot_process.stdin.flush()
            response = self.bot_out.readline().strip()
            return response
        elif method == 'POST':
            self.bot_process.stdin.write('POST\n')
            if data:
                self.bot_process.stdin.write(data + "\n")
            self.bot_process.stdin.flush()
            response = self.bot_out.readline().strip()
            return response
        else:
            return "Unsupported method"

    def stop(self):
        if self.bot_process is not None:
            self.bot_process.kill()



if __name__ == '__main__':
    # Dev test
    bot = BotPipe('./bots/random_bot.py')
    game = Game()

    dataJson = json.dumps(Serializer.get(game))
    response = bot.request(method='POST', data=dataJson)
    print(response)
import subprocess
import json

from packages.game_logic.game import Game
from packages.simulator.serializer import Serializer


class BotPipe:
    def __init__(self, bot_path: str):
        self.bot_process = None

        try:
            self.bot_process = subprocess.Popen(
                'python3 '+self.bot_path,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                text=True
            )

        except FileNotFoundError as e:
            print(f"Bot file not found: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def request(self, method, data=None):
        if method == 'GET':
            self.stdin.write("GET\n")
            self.stdin.flush()
            response = self.stdout.readline().strip()
            return response
        elif method == 'POST':
            self.stdin.write("POST\n")
            if data:
                self.stdin.write(data + "\n")
            self.stdin.flush()
            response = self.stdout.readline().strip()
            return response
        else:
            return "Unsupported method"

    def stop(self):
        if self.bot_process is not None:
            self.bot_process.kill()



if __name__ == '__main__':
    bot = BotPipe('./bots/random_bot.py')


    print(response)

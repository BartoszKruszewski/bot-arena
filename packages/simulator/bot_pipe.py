import subprocess
import json

class BotPipe:
    def __init__(self, bot: str):
        self.bot = bot
        self.bot_process = None

        try:
            self.bot_process = subprocess.Popen(
                'python3 '+self.bot,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                text=True  # Dodaj flagę 'text=True' dla poprawnego przesyłania tekstu
            )
        except FileNotFoundError as e:
            print(f"Bot file not found: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def stop(self):
        if self.bot_process is not None:
            self.bot_process.kill()

    def bot_message(self, message: str):
        if self.bot_process is not None:
            self.bot_process.stdin.write(message + "\n")
            self.bot_process.stdin.flush()

    def get_response(self) -> str:
        if self.bot_process is not None:
            response = self.bot_process.stdout.readline()
            return response
        else:
            return None

    def listen(self) -> str:
        response = self.get_response()
        while response is None:
            response = self.get_response()
        return response

    def get_request(self, message: str) -> str:
        if message is json:
            msg = json.loads(message)
        else:
            msg = message
        self.bot_message(json.dumps({'GET': msg}))
        return self.listen()

    def post_request(self, message: str):
        if message is json:
            msg = json.loads(message)
        else:
            msg = message
        self.bot_message(json.dumps({'POST': msg}))


if __name__ == '__main__':
    bot = BotPipe('./bots/random_bot.py')
    response = bot.post_request({'game_status' : {'xd':'wow'}})

    print(response)

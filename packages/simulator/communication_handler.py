import subprocess
import json

class CommunicationHandler:

    def __init__(self,bot :str):
        self.bot = bot

        self.bot_process = None
        self.bot_to_game = None
        self.game_to_bot = None


    def start(self):
        try:
            self.bot_process = subprocess.Popen(self.bot, stdin=subprocess.PIPE,
                                                stdout=subprocess.PIPE, text=True)

            self.bot_to_game = self.bot_process.stdout
            self.game_to_bot = self.bot_process.stdin

        except FileNotFoundError as e:
            print(f"Bot file not found: {str(e)}")
        except BrokenPipeError as e:
            print(f"Broken pipe error: {str(e)}")


    def stop(self):
        if self.bot_process is not None:
            self.bot_process.kill()

    def bot_message(self, message: json):
        self.game_to_bot.write(message)
    def get_request(self, message: json):
        msg = json.loads(message)
        msg = {'GET': msg}
        self.bot_message(json.dumps(msg))

    def get_response(self) -> json:
        try:
            response = self.bot_to_game.communicate()
            if type(response) is not json:
                return response
            else:
                raise Exception("Invalid file format")

        except Exception as e:
            print(f"File format error. {str(e)}")

    def listen(self) -> json:
        response = self.get_message()
        while response is None:
            response = self.get_message()

        return response
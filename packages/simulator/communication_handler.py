import subprocess
import json

class CommunicationHandler:

    def __init__(self,bot_left :str,bot_right :str):
        self.bot_left = bot_left
        self.bot_right = bot_right

        self.bot_left_process = None
        self.bot_right_process = None

        self.bot_left_to_game = None
        self.bot_right_to_game = None

        self.game_to_bot_left = None
        self.game_to_bot_right = None

    def start(self):
        try:
            self.bot_left_process = subprocess.Popen(self.bot_left, stdin=subprocess.PIPE,
                                                     stdout=subprocess.PIPE, text=True)
            self.bot_right_process = subprocess.Popen(self.bot_right, stdin=subprocess.PIPE,
                                                      stdout=subprocess.PIPE, text=True)

            self.bot_left_to_game = self.bot_left_process.stdout
            self.bot_right_to_game = self.bot_right_process.stdout

            self.game_to_bot_left = self.bot_left_process.stdin
            self.game_to_bot_right = self.bot_right_process.stdin

        except FileNotFoundError as e:
            print(f"Bot file not found: {str(e)}")
        except BrokenPipeError as e:
            print(f"Broken pipe error: {str(e)}")


    def stop(self):
        if self.bot_left_process is not None:
            self.bot_left_process.kill()
        if self.bot_left_process is not None:
            self.bot_right_process.kill()

    def bot_message(self, bot: str, message: json):
        try:
            if bot == 'left':
                self.game_to_bot_left.write(message)
            elif bot == 'right':
                self.game_to_bot_left.write(message)
            else:
                raise ValueError("Invalid value for the 'bot' parameter")

        except ValueError as e:
            print(f"Error: {str(e)}")



communication = CommunicationHandler('./bots/random_bot.py', './bots/random_bot.py')
communication.start()
communication.bot_message('left')
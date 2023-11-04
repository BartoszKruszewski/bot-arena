from flask import Flask, request
import json

from packages.game_logic.game import Game
from packages.simulator.serializer import Serializer

class ApiHandler:
    def __init__(self, game: Game):
        self.app = Flask(__name__)
        self._game = game

        self._last_command = {
            'left' : None,
            'right': None
        }


        @self.app.route('/game_status', methods=['GET'])
        def get_game_status():
            return Serializer.get(self._game)

        @self.app.route('/send_command', methods=['POST'])
        def send_command():
            bot_id = request.args.get('bot_id')
            command = request.data.decode('utf-8')


            if bot_id == 'bot1':
                self._last_command['left']
            elif bot_id == 'bot2':
                self._last_command['right']

            return command

        @self.app.route('/dev', methods=['GET'])
        def dev_endpoint():
            server_state = {
                'game_status': Serializer.get(self._game),
                'last_command': self._last_command
            }
            return json.dumps(server_state)

# Dev
if __name__ == "__main__":
    game_instance = Game()
    api = ApiHandler(game_instance)
    api.app.run(debug=True)
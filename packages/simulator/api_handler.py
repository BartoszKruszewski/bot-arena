from flask import Flask, request
import json

from packages.game_logic.game import Game
from packages.simulator.serializer import Serializer
class ApiHandler:
    def __init__(self, game: Game):
        self.app = Flask(__name__)

        self.last_command = None
        self._game = game


        @self.app.route('/game_status', methods=['GET'])
        def get_game_status():
            return Serializer.get(self._game)

        @self.app.route('/send_command', methods=['POST'])
        def send_command():
            self.last_command = request.data.decode('utf-8')
            return self.last_command

# Dev
if __name__ == "__main__":
    game_instance = Game()
    api = ApiHandler(game_instance)
    api.app.run(debug=True)

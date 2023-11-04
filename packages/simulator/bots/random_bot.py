import random
import time
import requests

class RandomBot:
    def __init__(self, api_url: str):
        self._api_url = api_url
        self._game_status = None

    def run(self):
        while True:
            self._game_status = self._get_game_status()

            if self._game_status is not None:
                self._send_command()

            time.sleep(2)

    def _get_game_status(self):
        response = requests.get(f"{self._api_url}/game_status")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Błąd przy pobieraniu stanu gry: {response.status_code}")
            return

    def _send_command(self):
        command = self._randomCommand()

        response = requests.post(f"{self._api_url}/send_command", command)
        # if response.status_code == 200:
        #     print(f"Wysłano komendę: {command}")
        # else:
        #     print(f"Błąd wysyłania komendy: {response.status_code}")

    def _randomCommand(self) -> str:
        coords = self._randomCoords()
        side = random.choice(['l', 'r'])

        commands = ['w', 'l', 'b', 'r', f't {side} {coords[0]} {coords[1]}']
        return random.choice(commands)

    def _randomCoords(self) -> tuple[int, int]:
        map_size = self._game_status['arena']['map_size']
        maxX = map_size[0]
        maxY = map_size[1]

        x = random.randint(0, maxX)
        y = random.randint(0, maxY)

        return (x,y)

# bot = RandomBot('http://127.0.0.1:5000')
# bot.run()

import random
import time
import requests
import threading


class RandomBot:
    def __init__(self, api_url: str, side: str):
        self._api_url = api_url
        self._game_status = None
        self._side = side

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
            print(f"{self._side}: Błąd przy pobieraniu stanu gry: {response.status_code}")
            return

    def _send_command(self):
        command = self._randomCommand()
        payload = {'side': self._side}

        response = requests.post(f"{self._api_url}/send_command", data=command, params=payload)
        if response.status_code == 200:
            print(f"{self._side}: Wysłano komendę: {command}")
        else:
            print(f"{self._side}: Błąd wysyłania komendy: {response.status_code}")

    def _randomCommand(self) -> str:
        coords = self._randomCoords()
        commands = ['w', 's', f't {coords[0]} {coords[1]}']

        return random.choice(commands)

    def _randomCoords(self) -> tuple[int, int]:
        map_size = self._game_status['arena']['map_size']
        maxX = map_size[0]
        maxY = map_size[1]

        x = random.randint(0, maxX)
        y = random.randint(0, maxY)

        return (x, y)


if __name__ == "__main__":
    bot1 = RandomBot('http://127.0.0.1:5000', side='left')
    bot2 = RandomBot('http://127.0.0.1:5000', side='right')

    thread1 = threading.Thread(target=bot1.run)
    thread2 = threading.Thread(target=bot2.run)

    thread1.start()
    thread2.start()

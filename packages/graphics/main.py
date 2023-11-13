from pygame import init, WINDOWCLOSE
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.transform import scale 

from .const import SCREEN_SIZE, FRAMERATE, STANDARD_FRAMERATE, ROUND_LEN
from .engine import Engine
from ..game_logic.game import Game
from os import name as os_name

from .log_interpreter import LogInterpreter

class Main:
    def __init__(self, log_name: str):
        init()
        self.__screen = display_set_mode(SCREEN_SIZE)
        self.__is_running = True
        self.__dt = 1
        self.__clock = Clock()
        self.__game = Game()
        self.__engine = Engine(self.__game)
        self.__tick = 0
        self.__game_speed = 2
        
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + "/../../logs/" + log_name
        if os_name == 'posix':
            path = "./logs/" + log_name

        log_interpreter = LogInterpreter(path)

        while self.__is_running:
            self.__is_running = WINDOWCLOSE not in map(lambda e: e.type, get_event())
            self.__tick += 1
            if self.__tick > FRAMERATE / self.__game_speed:
                game_output = self.__game.update(*log_interpreter.get_next_actions())
                self.__tick = 0
            self.__screen_update()

    def __screen_update(self):
        '''Refreshes screen and update frame clock.
        '''

        self.__dt = self.__clock.tick(FRAMERATE) * STANDARD_FRAMERATE / 1000
        self.__screen.blit(scale(self.__engine.render(self.__game, self.__game_speed), SCREEN_SIZE), (0, 0))
        display_update()

    def set_game_speed(self, value: float) -> None:
        '''Game speed setter.

        Value must be greater than 0 and lower or equal FRAMERATE.
        '''

        if value <= 0:
            raise Exception('Game speed must be greater than zero!')
        elif value > FRAMERATE:
            raise Exception('Game speed cannot be greater than FRAMERATE!')
        self.__game_speed = value

    def get_game_speed(self) -> float:
        '''Game speed getter.
        '''
        return self.__game_speed

if __name__ == "__main__":
    Main()

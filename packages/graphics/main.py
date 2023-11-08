from pygame import init, WINDOWCLOSE
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.transform import scale 

from .const import SCREEN_SIZE, FRAMERATE, STANDARD_FRAMERATE, ROUND_LEN
from .engine import Engine
from ..game_logic.game import Game

from .log_interpreter import LogInterpreter

class Main:
    def __init__(self, log_name: str):
        init()
        self.screen = display_set_mode(SCREEN_SIZE)
        self.is_running = True
        self.dt = 1
        self.clock = Clock()
        self.game = Game()
        self.engine = Engine(self.game)
        self.tick = 0
        
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + "/../../logs/" + log_name

        log_interpreter = LogInterpreter(path)

        while self.is_running:
            self.is_running = WINDOWCLOSE not in map(lambda e: e.type, get_event())
            self.tick += 1
            if self.tick > FRAMERATE * ROUND_LEN / 1000:
                game_output = self.game.update(*log_interpreter.get_next_actions())
                print(__name__, game_output)
                self.tick = 0
            self.__screen_update()

    def __screen_update(self):
        '''Refreshes screen and update frame clock.
        '''

        self.dt = self.clock.tick(FRAMERATE) * STANDARD_FRAMERATE / 1000
        self.screen.blit(scale(self.engine.render(self.game), SCREEN_SIZE), (0, 0))
        display_update()

if __name__ == "__main__":
    Main()

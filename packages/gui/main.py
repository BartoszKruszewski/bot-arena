from .scene_example.manager import Manager as ExampleManager
from .scene_main.main_manager import Manager as MainManager
from .scene_game.manager import Manager as GameManager
from ..game_logic.game import Game

from .const import SCREEN_SIZE, FRAMERATE
from .mouse import Mouse

from pygame import WINDOWCLOSE, init
from pygame.time import Clock
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.event import peek as event_peek
from pygame.event import get as event_get

class ManagerInfo:
    def __init__(self):
        self.events = []

class Main():
    def __init__(self, log_name: str):
        init()
        self.screen = display_set_mode(SCREEN_SIZE)
        self.is_running = True
        self.clock = Clock()
        self.mouse = Mouse()

        self.manager = MainManager(
            self.load_example_scene,
            self.load_another_scene,
            self.load_another_another_scene,
            self.load_game_scene
        )

        while self.is_running:
            self.is_running = not event_peek(WINDOWCLOSE)
            
            self.mouse.update()

            manager_info = ManagerInfo()
            manager_info.events = event_get()

            dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000
            self.screen.blit(self.manager(manager_info, dt, self.mouse), (0, 0))
            display_update()

    def load_example_scene(self):
        self.manager = ExampleManager(self.go_back)

    def load_another_scene(self):
        self.manager = ExampleManager(self.go_back)

    def load_another_another_scene(self):
        self.manager = ExampleManager(self.go_back)

    def load_game_scene(self):
        self.manager = GameManager(self.go_back)

    def go_back(self):
        print('go back')

    



        

        

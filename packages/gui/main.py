from packages.gui.scenes.example_scene import ExampleSceneManager
from packages.gui.scenes.game_scene import GameSceneManager
from packages.gui.scenes.main_scene import MainSceneManager
from ..game_logic.game import Game

from .const import SCREEN_SIZE, FRAMERATE

from pygame import WINDOWCLOSE, init
from pygame.time import Clock
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.event import peek as event_peek
from pygame.event import get as event_get

class ManagerInfo:
    def __init__(self):
        self.events = []

class Main():
    def __init__(self):
        init()
        self.screen = display_set_mode(SCREEN_SIZE)
        self.is_running = True
        self.clock = Clock()

        self.manager = MainSceneManager({
            'example': self.load_example_scene,
            'game': self.load_game_scene,
        })

        while self.is_running:
            self.is_running = not event_peek(WINDOWCLOSE)

            manager_info = ManagerInfo()
            manager_info.events = event_get()

            dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000
            self.screen.blit(self.manager(manager_info, dt), (0, 0))
            display_update()

    def load_game_scene(self):
        self.manager = GameSceneManager(self.go_back)

    def load_example_scene(self):
        self.manager = ExampleSceneManager(self.go_back)

    def go_back(self):
        print('go back')

    



        

        

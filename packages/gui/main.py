from packages.gui.scenes.example_scene import ExampleSceneManager
from packages.gui.scenes.game_scene import GameSceneManager
from packages.gui.scenes.game_end_scene import GameEndSceneManager
from packages.gui.scenes.main_scene import MainSceneManager

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
        self.thread = None

        self.load_main_scene()

        while self.is_running:
            self.is_running = not event_peek(WINDOWCLOSE)

            manager_info = ManagerInfo()
            manager_info.events = event_get()

            dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000
            surf, self.thread = self.manager(manager_info, dt, self.thread)
            self.screen.blit(surf, (0, 0))
            display_update()

    def load_game_scene(self):
        self.manager = GameSceneManager({'game_end': self.load_game_end_scene})

    def load_example_scene(self):
        self.manager = ExampleSceneManager({'main': self.load_main_scene})

    def load_game_end_scene(self):
        self.manager = GameEndSceneManager({'main': self.load_main_scene})

    def load_main_scene(self):
        self.manager = MainSceneManager({
            'example': self.load_example_scene,
            'game': self.load_game_scene,
        })

    



        

        

from packages.gui.scenes.game_scene import GameSceneManager
from packages.gui.scenes.simulation_scene import SimulationSceneManager

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

        self.load_simulation_scene()
        #self.load_game_scene('cos')

        while self.is_running:
            self.is_running = not event_peek(WINDOWCLOSE)

            manager_info = ManagerInfo()
            manager_info.events = event_get()

            dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000
            surf, self.thread = self.manager(manager_info, dt, self.thread)
            self.screen.blit(surf, (0, 0))
            display_update()

    def load_game_scene(self, log_name):
        self.manager = GameSceneManager({'simulation': self.load_simulation_scene, 'log_name': log_name})

    def load_simulation_scene(self):
        self.manager = SimulationSceneManager({'game': self.load_game_scene})

    



        

        

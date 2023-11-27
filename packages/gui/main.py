from .scene_example.manager import Manager as ExampleManager
from .scene_main.main_manager import Manager as MainManager

from .const import SCREEN_SIZE

from pygame import WINDOWCLOSE, init
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

        self.manager = MainManager(self.load_example_scene, self.load_another_scene, self.load_another_another_scene)

        while self.is_running:
            self.is_running = not event_peek(WINDOWCLOSE)

            manager_info = ManagerInfo()
            manager_info.events = event_get()

            self.screen.blit(self.manager(manager_info), (0, 0))
            display_update()

    def load_example_scene(self):
        self.manager = ExampleManager(self.go_back)

    def load_another_scene(self):
        self.manager = ExampleManager(self.go_back)

    def load_another_another_scene(self):
        self.manager = ExampleManager(self.go_back)

    def go_back(self):
        print('go back')

    



        

        

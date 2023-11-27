from .scene1 import load_scene
from ..const import SCREEN_SIZE

class Manager:
    def __init__(self, go_back_function):
        self.scene = load_scene()
        self.scene.calc_pos((0, 0), SCREEN_SIZE)

        self.another_scene = None

    def funny_function(self):
        pass 

    def __call__(self, manager_info):
        for event in manager_info.events:
            self.scene.handle_event(event)
        return self.scene.render()

    
        
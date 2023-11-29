from .const import SCREEN_SIZE
from abc import ABC

class AbstractSceneManager(ABC):
    def __init__(self, scene_functions = {}):
        self.scene = self.load_scene(scene_functions)
        self.scene.calc_pos((0, 0), SCREEN_SIZE)

    def __call__(self, manager_info, dt):
        for event in manager_info.events:
            self.scene.handle_event(event)
        self.scene.update(dt)
        return self.scene.render()
    
    def load_scene(self, scene_functions):
        pass
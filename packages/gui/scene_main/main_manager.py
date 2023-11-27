from ..const import SCREEN_SIZE
from .scene import load_scene

class Manager:
    def __init__(self, scene1_function, scene2_function, scene3_function):
        self.scene = load_scene(scene1_function, scene2_function, scene3_function)

        self.scene.calc_pos((0, 0), SCREEN_SIZE)

    def __call__(self, manager_info):
        for event in manager_info.events:
            self.scene.handle_event(event)
        return self.scene.render()

    
        
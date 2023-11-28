from ..const import SCREEN_SIZE
from .scene import load_scene

class Manager:
    def __init__(self, go_back_function):
        self.scene = load_scene()
        self.scene.calc_pos((0, 0), SCREEN_SIZE)

    def __call__(self, manager_info, dt, mouse):
        for event in manager_info.events:
            self.scene.handle_event(event)
        return self.scene.render(dt, mouse)
from abc import ABC
from packages.gui.gui_objects import Scene, Text
from threading import Thread

class AbstractSceneManager(ABC):
    def __init__(self, scene_functions = {}):
        self.scene = Scene([
            Text((0, 0), (0.2, 0.2), text = 'loading...', color='white')
        ], name='loading')
        self.initialized = False
        self.scene_functions = scene_functions

    def __call__(self, manager_info, dt, thread):
        for event in manager_info.events:
            self.scene.handle_event(event)
        if not self.initialized:
            self.initialized = True
            def thread_function():
                self.scene = self.load_scene(self.scene_functions)
            thread = Thread(target = thread_function)
            thread.start()
        self.scene.update(dt)
        return self.scene.render(), thread

    def load_scene(self, scene_functions):
        pass
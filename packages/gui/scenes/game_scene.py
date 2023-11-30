from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, GameRenderer

class GameSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([], (0, 0), (0.2, 1), color=(42, 42, 42)),
            Window([ 
                    GameRenderer((0, 0), (1, 1))
                ], (0.2, 0), (0.8, 0.8), color=(84, 84, 84)),
            Window([], (0.2, 0.8), (1, 0.2), color=(126, 126, 126)),
        ])
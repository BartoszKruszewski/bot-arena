from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, Button

class GameEndSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([ 
                    Button(
                        (0.45, 0.1),
                        (0.1, 0.1),
                        color = (255, 0, 0),
                        text = 'go back',
                        on_click = scene_functions['main']
                    )
                ], (0, 0), (1, 1), color=(84, 84, 84)),
        ])
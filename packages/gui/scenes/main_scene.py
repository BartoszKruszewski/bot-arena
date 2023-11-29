from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects.scene import Scene
from packages.gui.gui_objects.button import Button

class MainSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Button(
                (0.3, 0.4), (0.4, 0.1),
                color=(255, 255, 0),
                on_click=scene_functions['game']
            ),
            Button(
                (0.3, 0.6), (0.4, 0.1),
                color=(0, 0, 255),
                on_click=scene_functions['example']
            ),
        ])
    
from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Scene, Button, Window

PROPORTION1 = 0.6
PROPORTION2 = 0.6



class SimulationSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([], (0, 0), (PROPORTION1 / 2, 1), color=(42, 42, 42), name = 'bots'),
            Window([], (PROPORTION1 / 2, 0), (PROPORTION1 / 2, 1), color=(84, 84, 84), name = 'maps'),
            Window([], (PROPORTION1, 0), (1 - PROPORTION1, PROPORTION2), color=(42, 42, 42), name = 'control'),
            Window([
                Button(
                    (0.3, 0.4), (0.4, 0.1),
                    color=(255, 255, 0),
                    on_click=scene_functions['game']
                ),
            ], (PROPORTION1, PROPORTION2), (1 - PROPORTION1, 1 - PROPORTION2), color=(126, 126, 126), name = 'progres'),
        ], name = 'choose simulation')
    
from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Scene, Button, Window, List, NumberField, Text
from os import listdir
from packages import MAPS_DIRECTORY, BOTS_DIRECTORY

PROPORTION1 = 0.6
PROPORTION2 = 0.6

class SimulationSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
                List(
                    listdir(BOTS_DIRECTORY),
                    (0, 0), (PROPORTION1 / 2, 1),
                    color=(42, 42, 42),
                    name = 'bots',
                    on_click = self.add_bot,
                    max_active = 2
                ),
                List(
                    listdir(MAPS_DIRECTORY),
                    (PROPORTION1 / 2, 0), (PROPORTION1 / 2, 1),
                    color=(84, 84, 84),
                    name = 'maps',
                    on_click = self.add_map,
                    max_active = 1
                ),
                Window([
                        NumberField((0, 0), (0.3, 0.3), name = 'number of simulations'),
                        Text((0, 0.4), (1, 0.1), text = "empty bot1", font_size = 30, id='bot1'),
                        Text((0, 0.6), (1, 0.1), text = "empty bot2", font_size = 30, id='bot2'),
                        Text((0, 0.8), (1, 0.1), text = "empty map", font_size = 30, id='map')
                    ], 
                    (PROPORTION1, 0), (1 - PROPORTION1, PROPORTION2),
                    color=(42, 42, 42), name = 'control'
                ),
                Window([
                        Button(
                            (0.3, 0.4), (0.4, 0.1),
                            color=(255, 255, 0),
                            on_click=scene_functions['game']
                        ),
                    ], 
                    (PROPORTION1, PROPORTION2), (1 - PROPORTION1, 1 - PROPORTION2),
                    color=(126, 126, 126), name = 'progres'
                ),
            ], 
            name = 'choose simulation'
        )
    
    def add_bot(self, active_buttons):
        if len(active_buttons) == 0:
            self.scene.send_info('bot1', 'text', 'empty bot1')
            self.scene.send_info('bot2', 'text', 'empty bot2')
        elif len(active_buttons) == 1:
            self.scene.send_info('bot1', 'text', active_buttons[0])
            self.scene.send_info('bot2', 'text', 'empty bot2')
        elif len(active_buttons) == 2:
            self.scene.send_info('bot1', 'text', active_buttons[0])
            self.scene.send_info('bot2', 'text', active_buttons[1])


    def add_map(self, active_buttons):
        if len(active_buttons) == 0:
            self.scene.send_info('map', 'text', 'empty map')
        elif len(active_buttons) == 1:
            self.scene.send_info('map', 'text', active_buttons[0])
    
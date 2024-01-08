from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, GameRenderer, Button, RadioButton
from packages.gui.const import GUI_COLORS

PROPORTION1 = 0.22
PROPORTION2 = 0.4

class GameSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([],
                (0, 0), (PROPORTION1, 1 - PROPORTION1),
                color=(42, 42, 42),
                name = 'log',
                icon = 'console'
            ),
            Window([ 
                GameRenderer(
                    (0, 0),
                    (1, 1),
                    game_end_action = scene_functions['simulation'],
                    id = 'game_renderer',
                    log_name = scene_functions['log_name']
                )
            ], 
                (PROPORTION1, 0), (1 - PROPORTION1, 1 - PROPORTION1), 
                color=(84, 84, 84),
                name = 'game',
                icon = 'game',
            ),
            Window([], 
                (0, 1 - PROPORTION1), (PROPORTION2, PROPORTION1), 
                color=(42, 42, 42), 
                name = 'stats',
                icon = 'stats',
                background_color = GUI_COLORS['background2'],
                headerbar_color = GUI_COLORS['background1']
            ),
            Window([
                Button(
                    (0.45, 0.45),
                    (0.3, 0.3),
                    text = 'end_game',
                    color = (0, 0, 255),
                    on_click = scene_functions['simulation']
                ),
                Button(
                    (0.1, 0.1),
                    (0.3, 0.3),
                    text = 'speed up',
                    color = (0, 255, 0),
                    on_click = self.increase_game_speed
                ),
                RadioButton(
                    (0.07, 0.5),
                    (0.1, 0.3),
                    text = 'area',
                    color = (255, 0, 90),
                    on_click = self.toggle_helper('obstacles_area')
                ),
                RadioButton(
                    (0.18, 0.5),
                    (0.1, 0.3),
                    text = 'pos',
                    color = (255, 155, 0),
                    on_click = self.toggle_helper('pos')
                ),
                RadioButton(
                    (0.29, 0.5),
                    (0.1, 0.3),
                    text = 'grid',
                    color = (255, 0, 0),
                    on_click = self.toggle_helper('grid')
                ),

            ], 
            (PROPORTION2, 1 - PROPORTION1), (1 - PROPORTION2, PROPORTION1),
            color=(126, 126, 126), 
            name = 'controls',
            icon = 'controls'
        ),
            
        ])
    
    def increase_game_speed(self):
        actual_game_speed = self.scene.get_info('game_renderer', 'game_speed')
        self.scene.send_info('game_renderer', 'game_speed', actual_game_speed + 1)

    def toggle_helper(self, helper):
        def toggler():
            helpers = self.scene.get_info('game_renderer', 'helpers')
            if helper in helpers:
                helpers.remove(helper)
            else:
                helpers.append(helper)
        return toggler
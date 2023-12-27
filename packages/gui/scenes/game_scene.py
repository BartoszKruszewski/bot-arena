from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, GameRenderer, Button, RadioButton

class GameSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([], (0, 0), (0.2, 1), color=(42, 42, 42), name = 'example2'),
            Window([ 
                GameRenderer(
                    (0, 0),
                    (1, 1),
                    game_end_action = scene_functions['game_end'],
                    id = 'game_renderer'
                )
                ], (0.2, 0), (0.8, 0.8), color=(84, 84, 84), name = 'game'),
            Window([
                Button(
                    (0.45, 0.45),
                    (0.3, 0.3),
                    text = 'end_game',
                    color = (0, 0, 255),
                    on_click = scene_functions['game_end']
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

            ], (0.2, 0.8), (1, 0.2), color=(126, 126, 126), name = 'example'),
        ], name = 'main')
    
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
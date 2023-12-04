from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, GameRenderer, Button, RadioButton

class GameSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([], (0, 0), (0.2, 1), color=(42, 42, 42)),
            Window([ 
                GameRenderer(
                    (0, 0),
                    (1, 1),
                    game_end_action = scene_functions['game_end'],
                    id = 'game_renderer'
                )
                ], (0.2, 0), (0.8, 0.8), color=(84, 84, 84)),
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
                    (0.1, 0.5),
                    (0.3, 0.3),
                    text = 'grid',
                    color = (255, 0, 0),
                    on_click = self.toggle_grid
                ),

            ], (0.2, 0.8), (1, 0.2), color=(126, 126, 126)),
        ])
    
    def increase_game_speed(self):
        actual_game_speed = self.scene.get_info('game_renderer', 'game_speed')
        self.scene.send_info('game_renderer', 'game_speed', actual_game_speed + 1)

    def toggle_grid(self):
        helpers = self.scene.get_info('game_renderer', 'helpers')
        if 'grid' in helpers:
            helpers.remove('grid')
        else:
            helpers.append('grid')
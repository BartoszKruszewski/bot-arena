from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, GameRenderer, Button, RadioButton, Text, Slider
from packages.gui.gui_objects.stats_display import StatsDisplay
from packages.gui.gui_objects.log_list import LogList
from packages.gui.const import GUI_COLORS, SPEED_CONTROL_STEP, SPEED_CONTROL_SLIDER_MULT, \
    ZOOM_CONTROL_STEP, ZOOM_CONTROL_SLIDER_MULT

PROPORTION1 = 0.22
PROPORTION2 = 0.4

CONTROLS_GAP1 = 0.06
CONTROLS_HEIGHT = 0.25
CONTROLS_WIDTH = 0.25 / (1 - PROPORTION2) * PROPORTION1 / 16 * 9

class GameSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([
                LogList(
                    (0, 0), (1, 1), scene_functions['log_name'], self.get_game_speed
                )
            ],
                (0, 0), (PROPORTION1, 1 - PROPORTION1),
                color=(42, 42, 42),
                name = 'log',
                icon = 'console'
            ),
            Window([ 
                GameRenderer(
                    (0, 0),
                    (1, 1),
                    game_end_action = scene_functions['log_select'],
                    id = 'game_renderer',
                    log_name = scene_functions['log_name']
                )
            ], 
                (PROPORTION1, 0), (1 - PROPORTION1, 1 - PROPORTION1), 
                color=(84, 84, 84),
                name = 'game',
                icon = 'game',
            ),
            StatsDisplay([
                Text((0.1, 0.4), (0.1, 0.15), "Left"),
                Text((0.1, 0.75), (0.1, 0.15), "Right"),
                Text((0.3, 0.05), (0.15, 0.15), "income"),
                Text((0.6, 0.05), (0.15, 0.15), "gold"),
                
                Text((0.3, 0.4), (0.15, 0.15), '0', id = "left_income"),
                Text((0.6, 0.4), (0.15, 0.15), '0', id = "left_gold"),
                Text((0.3, 0.75), (0.15, 0.15), '0', id = "right_income"),
                Text((0.6, 0.75), (0.15, 0.15), '0', id = "right_gold")
            ], 
                (0, 1 - PROPORTION1), (PROPORTION2, PROPORTION1), 
                self.update_dict,
                color=(42, 42, 42), 
                name = 'stats',
                icon = 'stats',
                background_color = GUI_COLORS['background2'],
                headerbar_color = GUI_COLORS['background1']
            ),
            Window([
                Text(
                    (CONTROLS_GAP1, CONTROLS_GAP1), 
                    (0.2, CONTROLS_HEIGHT),
                    text = "game speed:",
                ),
                Button(
                    (CONTROLS_GAP1 * 2 + 0.2, CONTROLS_GAP1),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'backward',
                    on_click = self.decrease_game_speed,
                ),
                RadioButton(
                    (CONTROLS_GAP1 * 2 + 0.2 + CONTROLS_WIDTH + 0.01, CONTROLS_GAP1),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'pause',
                    on_click = self.freeze
                ),
                Button(
                    (CONTROLS_GAP1 * 2 + 0.2 + CONTROLS_WIDTH * 2 + 0.01 * 2, CONTROLS_GAP1),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'forward',
                    on_click = self.increase_game_speed
                ),
                Slider(
                    (CONTROLS_GAP1 * 3 + 0.2 + CONTROLS_WIDTH * 3 + 0.01 * 3, CONTROLS_GAP1),
                    (0.25, CONTROLS_HEIGHT),
                    on_change = self.set_game_speed,
                    id = 'game_speed_slider'
                ),
                Text(
                    (CONTROLS_GAP1 * 3 + 0.45 + CONTROLS_WIDTH * 3 + 0.01 * 4, CONTROLS_GAP1),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    text = "1",
                    background_color = GUI_COLORS['background2'],
                    id = 'game_speed_info'
                ),
                Text(
                    (CONTROLS_GAP1, CONTROLS_GAP1 * 2 + CONTROLS_HEIGHT),
                    (0.2, CONTROLS_HEIGHT),
                    text = "zoom:",
                ),
                Button(
                    (CONTROLS_GAP1 * 2 + 0.2, CONTROLS_GAP1 * 2 + CONTROLS_HEIGHT),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'zoom_out',
                    on_click = self.decrease_zoom
                ),
                Button(
                    (CONTROLS_GAP1 * 2 + 0.305 + 0.01 * 2, CONTROLS_GAP1 * 2 + CONTROLS_HEIGHT),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'zoom_in',
                    on_click = self.increase_zoom
                ),
                Slider(
                    (CONTROLS_GAP1 * 3 + 0.2 + CONTROLS_WIDTH * 3 + 0.01 * 3, CONTROLS_GAP1 * 2 + CONTROLS_HEIGHT),
                    (0.25, CONTROLS_HEIGHT),
                    on_change = self.set_zoom,
                    id = 'zoom_slider'
                ),
                Text(
                    (CONTROLS_GAP1 * 3 + 0.45 + CONTROLS_WIDTH * 3 + 0.01 * 4, CONTROLS_GAP1 * 2 + CONTROLS_HEIGHT),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    text = "1",
                    background_color = GUI_COLORS['background2'],
                    id = 'zoom_info'
                ),
                Text(
                    (CONTROLS_GAP1, CONTROLS_GAP1 * 3 + CONTROLS_HEIGHT * 2), 
                    (0.2, CONTROLS_HEIGHT), 
                    text = "helpers:",
                ),
                
                RadioButton(
                    (CONTROLS_GAP1 * 2 + 0.2, CONTROLS_GAP1 * 3 + CONTROLS_HEIGHT * 2),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'view',
                    color = (255, 0, 90),
                    on_click = self.toggle_helper('obstacles_area')
                ),
                RadioButton(
                    (CONTROLS_GAP1 * 2 + 0.2 + CONTROLS_WIDTH + 0.01, CONTROLS_GAP1 * 3 + CONTROLS_HEIGHT * 2),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'position',
                    color = (255, 155, 0),
                    on_click = self.toggle_helper('pos')
                ),
                RadioButton(
                    (CONTROLS_GAP1 * 2 + 0.2 + CONTROLS_WIDTH * 2 + 0.01 * 2, CONTROLS_GAP1 * 3 + CONTROLS_HEIGHT * 2),
                    (CONTROLS_WIDTH, CONTROLS_HEIGHT),
                    button_image = 'grid',
                    color = (255, 0, 0),
                    on_click = self.toggle_helper('grid')
                ),
                Button(
                    (CONTROLS_GAP1 * 3 + 0.2 + CONTROLS_WIDTH * 3 + 0.01 * 3, CONTROLS_GAP1 * 3 + CONTROLS_HEIGHT * 2),
                    (0.25, CONTROLS_HEIGHT),
                    text = 'close visualization',
                    color = (0, 0, 255),
                    on_click = scene_functions['log_select']
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
        if actual_game_speed > 0:
            self.scene.send_info('game_renderer', 'game_speed', actual_game_speed + SPEED_CONTROL_STEP)
            self.update_game_speed_info()

    def decrease_game_speed(self):
        actual_game_speed = self.scene.get_info('game_renderer', 'game_speed')
        if actual_game_speed > 0:
            self.scene.send_info('game_renderer', 'game_speed', actual_game_speed - SPEED_CONTROL_STEP)
            self.update_game_speed_info()

    def set_game_speed(self, value):
        actual_game_speed = self.scene.get_info('game_renderer', 'game_speed')
        if actual_game_speed > 0:
            self.scene.send_info('game_renderer', 'game_speed', (value + 0.5) ** SPEED_CONTROL_SLIDER_MULT)
            self.update_game_speed_info()

    def freeze(self):
        actual_game_speed = self.scene.get_info('game_renderer', 'game_speed')
        if actual_game_speed == 0:
            self.scene.send_info('game_renderer', 'game_speed', self.last_game_speed)
        else:
            self.last_game_speed = self.scene.get_info('game_renderer', 'game_speed')
            self.scene.send_info('game_renderer', 'game_speed', 0)
        self.update_game_speed_info()

    def update_game_speed_info(self):
        actual_game_speed = self.scene.get_info('game_renderer', 'game_speed')
        self.scene.send_info('game_speed_info', 'text', f'{actual_game_speed:.2f}')
        game_speed_slider_update_func = self.scene.get_info('game_speed_slider', 'update_slider_pos')
        game_speed_slider_update_func(actual_game_speed ** (1 / SPEED_CONTROL_SLIDER_MULT) - 0.5)

    def increase_zoom(self):
        actual_zoom = self.scene.get_info('game_renderer', 'zoom')
        self.scene.send_info('game_renderer', 'zoom', actual_zoom + ZOOM_CONTROL_STEP)
        self.update_zoom_info()

    def decrease_zoom(self):
        actual_zoom = self.scene.get_info('game_renderer', 'zoom')
        self.scene.send_info('game_renderer', 'zoom', actual_zoom - ZOOM_CONTROL_STEP)
        self.update_zoom_info()

    def set_zoom(self, value):
        actual_zoom = self.scene.get_info('game_renderer', 'zoom')
        self.scene.send_info('game_renderer', 'zoom', (value + 1.4) ** ZOOM_CONTROL_SLIDER_MULT)
        self.update_zoom_info()

    def update_zoom_info(self):
        actual_zoom = self.scene.get_info('game_renderer', 'zoom')
        self.scene.send_info('zoom_info', 'text', f'{actual_zoom:.2f}')
        zoom_slider_update_func = self.scene.get_info('zoom_slider', 'update_slider_pos')
        zoom_slider_update_func(actual_zoom ** (1 / ZOOM_CONTROL_SLIDER_MULT) - 1.4)

    def update_dict(self):
        return self.scene.get_info('game_renderer', 'game_stats')

    def get_game_speed(self):
        return self.scene.get_info('game_renderer', 'game_speed')
    
    def toggle_helper(self, helper):
        def toggler():
            helpers = self.scene.get_info('game_renderer', 'helpers')
            if helper in helpers:
                helpers.remove(helper)
            else:
                helpers.append(helper)
        return toggler
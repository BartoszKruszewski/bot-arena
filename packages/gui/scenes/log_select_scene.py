from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, Button, RadioButton, Text, Slider, List
from packages import LOGS_DIRECTORY
from packages.gui.const import GUI_COLORS
from os import listdir

PROPORTION1 = 0.6
PROPORTION2 = 0.7

CONTROLS_GAP1 = 0.04
CONTROLS_HEIGHT = 0.25

SIDEBAR_SIZE = 0.05

class LogSelectSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([
                Button(
                    (0.1, 0.01), (0.8, SIDEBAR_SIZE * 0.8 * 16 / 9),
                    blocked = True,
                    text = 'log',
                ),
                Button(
                    (0.1, 0.1), (0.8, SIDEBAR_SIZE * 0.8 * 16 / 9),
                    on_click = scene_functions['simulation'],
                    text = 'simulation',
                ),
            ], (0, 0), (SIDEBAR_SIZE, 1), name = ""),
            Window([
                List(
                    listdir(LOGS_DIRECTORY),
                    (0, 0), (1, 1),
                    on_click = self.simulation_select,
                    max_active = 1,
                    element_color = (0, 0, 0, 0),
                    id = 'simulations_list'
                )
            ], (SIDEBAR_SIZE, 0), ((PROPORTION1 - SIDEBAR_SIZE) / 2, 1), name = 'simulations', icon='bot'),
            Window([
                    List(
                    [],
                    (0.01, 0), (0.99, 1),
                    max_active = 1,
                    element_color = (0, 0, 0, 0),
                    on_click = self.log_select,
                    id = 'logs_list'
                ),
            ], (SIDEBAR_SIZE + (PROPORTION1 - SIDEBAR_SIZE) / 2, 0), ((PROPORTION1 - SIDEBAR_SIZE) / 2, 1),
                    name = 'logs', icon='map'),
            Window([
                Text((0.05, CONTROLS_GAP1), (0.2, 0.1), text = "simulation:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1), (0.65, 0.1),
                    text = "none", id='simulation_name',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 2 + 0.1), (0.2, 0.1), text = "log:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 2 + 0.1), (0.65, 0.1),
                    text = "none", id='log_name',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 3 + 0.2), (0.2, 0.1), text = "map:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 3 + 0.2), (0.65, 0.1),
                    text = "none", id='map',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 4 + 0.3), (0.2, 0.1), text = "bot1:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 4 + 0.3), (0.65, 0.1),
                    text = "none", id='bot1',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 5 + 0.4), (0.2, 0.1), text = "bot2:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 5 + 0.4), (0.65, 0.1),
                    text = "none", id='bot2',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 6 + 0.5), (0.2, 0.1), text = "winner:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 6 + 0.5), (0.65, 0.1),
                    text = "none", id='winner',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),

            
            ], (PROPORTION1, 0), (1 - PROPORTION1, PROPORTION2),
                    name = 'log info',
                    icon = 'simulation'
            ),
            Window([
                Button(
                    (0.1, 0.35), (0.8, 0.3),
                    on_click = self.run_visualization,
                    text = 'open visualization',
                    blocked = True,
                    id = 'run_button'
                ),
            ], (PROPORTION1, PROPORTION2), (1 - PROPORTION1, 1- PROPORTION2),
                    name = 'control',
                    icon = 'simulation'
            ),
        ])
    
    def simulation_select(self, active_buttons):
        if len(active_buttons) == 1:
            logs = listdir(f'{LOGS_DIRECTORY}/{active_buttons[0]}')
            self.scene.get_info('logs_list', 'set_elements')(logs)
            self.scene.send_info('simulation_name', 'text', active_buttons[0])
        else:
            self.scene.get_info('logs_list', 'set_elements')([])
            self.scene.send_info('simulation_name', 'text', 'none')
            self.scene.send_info('log_name', 'text', 'none')
            self.scene.send_info('map', 'text', 'none')
            self.scene.send_info('bot1', 'text', 'none')
            self.scene.send_info('bot2', 'text', 'none')
            self.scene.send_info('winner', 'text', 'none')
            self.scene.send_info('run_button', 'blocked', True)

    def log_select(self, active_buttons):
        if len(active_buttons) == 1:
            simulation = self.scene.get_info('simulation_name', 'text')
            with open(f'{LOGS_DIRECTORY}/{simulation}/{active_buttons[0]}') as f:
                map, bot1, bot2, winner = tuple([l.rstrip() for l in f.readlines()[:4]])
            self.scene.send_info('log_name', 'text', active_buttons[0])
            self.scene.send_info('run_button', 'blocked', False)
            self.scene.send_info('map', 'text', map)
            self.scene.send_info('bot1', 'text', bot1)
            self.scene.send_info('bot2', 'text', bot2)
            self.scene.send_info('winner', 'text', winner)
        else:
            self.scene.send_info('log_name', 'text', 'none')
            self.scene.send_info('map', 'text', 'none')
            self.scene.send_info('bot1', 'text', 'none')
            self.scene.send_info('bot2', 'text', 'none')
            self.scene.send_info('winner', 'text', 'none')
            self.scene.send_info('run_button', 'blocked', True)
    
    def run_visualization(self):
        simulation = self.scene.get_info('simulation_name', 'text')
        log = self.scene.get_info('log_name', 'text')
        self.scene_functions['game'](f'{simulation}/{log}')
        
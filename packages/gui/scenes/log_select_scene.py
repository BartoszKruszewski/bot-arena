from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Window, Scene, Button, RadioButton, Text, Slider, List, ProgressBar
from packages import LOGS_DIRECTORY
from packages.gui.const import GUI_COLORS
from os import listdir, path

PROPORTION1 = 0.65

CONTROLS_GAP1 = 0.045
CONTROLS_GAP2 = 0.06
CONTROLS_HEIGHT = 0.25

SIDEBAR_SIZE = 0.05

class LogSelectSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([
                Button(
                    (0.1, 0.01), (0.8, SIDEBAR_SIZE * 0.8 * 16 / 9),
                    blocked = True,
                    button_image = 'play',
                ),
                Button(
                    (0.1, 0.1), (0.8, SIDEBAR_SIZE * 0.8 * 16 / 9),
                    on_click = scene_functions['simulation'],
                    button_image = 'settings',
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
            ], (SIDEBAR_SIZE, 0), ((PROPORTION1 - SIDEBAR_SIZE) / 2, 1), name = 'simulations', icon='folder'),
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
                    name = 'logs', icon='log'),
            Window([
                Text((0.05, CONTROLS_GAP1), (0.2, 0.11), text = "name:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1), (0.65, 0.11),
                    text = "none", id='simulation_name',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 2 + 0.11), (0.2, 0.11), text = "map:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 2 + 0.11), (0.65, 0.11),
                    text = "none", id='map',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 3 + 0.22), (0.2, 0.11), text = "bot1:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 3 + 0.22), (0.65, 0.11),
                    text = "none", id='bot1',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 4 + 0.33), (0.35, 0.11), text = "bot1 won games:", background_color = GUI_COLORS['blocked']),
                ProgressBar(
                    (0.42, CONTROLS_GAP1 * 4 + 0.33), (0.36, 0.11),
                    id = 'bot1_won_progress_bar',
                ),
                Text((0.8, CONTROLS_GAP1 * 4 + 0.33), (0.15, 0.11), text = "0", background_color = GUI_COLORS['blocked'], id='bot1_wins'),
                Text((0.05, CONTROLS_GAP1 * 5 + 0.44), (0.2, 0.11), text = "bot2:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP1 * 5 + 0.44), (0.65, 0.11),
                    text = "none", id='bot2',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP1 * 6 + 0.55), (0.35, 0.11), text = "bot2 won games:", background_color = GUI_COLORS['blocked']),
                ProgressBar(
                    (0.42, CONTROLS_GAP1 * 6 + 0.55), (0.36, 0.11),
                    id = 'bot2_won_progress_bar',
                ),
                Text((0.8, CONTROLS_GAP1 * 6 + 0.55), (0.15, 0.11), text = "0", background_color = GUI_COLORS['blocked'], id='bot2_wins'),
            
            ], (PROPORTION1, 0), (1 - PROPORTION1, 0.6),
                    name = 'simulation info',
                    icon = 'info'
            ),
            Window([
                Text((0.05, CONTROLS_GAP2), (0.2, 0.17), text = "name:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP2), (0.65, 0.17),
                    text = "none", id='log_name',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP2 * 2 + 0.17), (0.2, 0.17), text = "winner:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP2 * 2 + 0.17), (0.65, 0.17),
                    text = "none", id='winner',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Text((0.05, CONTROLS_GAP2 * 3 + 0.34), (0.2, 0.17), text = "length:", background_color = GUI_COLORS['blocked']),
                Text(
                    (0.3, CONTROLS_GAP2 * 3 + 0.34), (0.65, 0.17),
                    text = "none", id='length',
                    background_color = GUI_COLORS['blocked'],
                    text_color = GUI_COLORS['button']
                ),
                Button(
                    (0.1, CONTROLS_GAP2 * 4 + 0.51), (0.8, 0.17),
                    on_click = self.run_visualization,
                    text = 'open visualization',
                    blocked = True,
                    id = 'run_button'
                ),
            ], (PROPORTION1, 0.6), (1 - PROPORTION1, 0.4),
                    name = 'log info',
                    icon = 'info'
            ),
        ])
    
    def set_progress_bar_state(self, bar_name, state):
        self.scene.send_info(bar_name, 'state', min(max(state, 0), 1))

    def simulation_select(self, active_buttons):
        if len(active_buttons) == 1:
            logs = listdir(path.join(LOGS_DIRECTORY, active_buttons[0]))
            bot1_wins = 0
            bot2_wins = 0
            with open(path.join(LOGS_DIRECTORY, active_buttons[0], logs[0])) as f:
                map, bot1, bot2 = tuple([l.rstrip() for l in f.readlines()[:3]])
            for log in logs:
                if log[-5] == '0':
                    bot1_wins += 1
                else:
                    bot2_wins += 1
            self.scene.send_info('map', 'text', map[4:])
            self.scene.send_info('bot1', 'text', bot1[8:])
            self.scene.send_info('bot2', 'text', bot2[8:])
            self.scene.send_info('bot1_wins', 'text', str(bot1_wins))
            self.scene.send_info('bot2_wins', 'text', str(bot2_wins))
            self.set_progress_bar_state('bot1_won_progress_bar', bot1_wins / (bot1_wins + bot2_wins))
            self.set_progress_bar_state('bot2_won_progress_bar', bot2_wins / (bot1_wins + bot2_wins))
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
            self.scene.send_info('length', 'text', 'none')
            self.scene.send_info('bot1_wins', 'text', '0')
            self.scene.send_info('bot2_wins', 'text', '0')
            self.set_progress_bar_state('bot1_won_progress_bar', 0)
            self.set_progress_bar_state('bot2_won_progress_bar', 0)



    def log_select(self, active_buttons):
        if len(active_buttons) == 1:
            simulation = self.scene.get_info('simulation_name', 'text')
            with open(path.join(LOGS_DIRECTORY, simulation, active_buttons[0])) as f:
                data = f.readlines()
                map, bot1, bot2 = tuple([l.rstrip() for l in data[:3]])
            winner = bot1 if active_buttons[0][-5] == '0' else bot2
            self.scene.send_info('log_name', 'text', active_buttons[0])
            self.scene.send_info('run_button', 'blocked', False)
            self.scene.send_info('winner', 'text', winner[8:])
            self.scene.send_info('length', 'text', str(len(data) - 4))
        else:
            self.scene.send_info('log_name', 'text', 'none')
            self.scene.send_info('winner', 'text', 'none')
            self.scene.send_info('run_button', 'blocked', True)
            self.scene.send_info('length', 'text', 'none')
    
    def run_visualization(self):
        simulation = self.scene.get_info('simulation_name', 'text')
        log = self.scene.get_info('log_name', 'text')
        self.scene_functions['game'](f'{simulation}/{log}')
        
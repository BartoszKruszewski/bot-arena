from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Scene, Button, Window, List, NumberField, Text, ProgressBar, RadioButton, InputField
from os import listdir
from packages import MAPS_DIRECTORY, BOTS_DIRECTORY
from packages.simulator.api import play
from threading import Thread
from packages.gui.const import GUI_COLORS

PROPORTION1 = 0.6
PROPORTION2 = 0.6

CONTROLS_GAP1 = 0.02
CONTROLS_GAP2 = 0.06

class SimulationSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
                List(
                    listdir(BOTS_DIRECTORY),
                    (0, 0), (PROPORTION1 / 2, 1),
                    name = 'bots',
                    on_click = self.add_bot,
                    max_active = 2,
                    element_color = (0, 0, 0, 0),
                    icon='bot'
                ),
                List(
                    listdir(MAPS_DIRECTORY),
                    (PROPORTION1 / 2, 0), (PROPORTION1 / 2, 1),
                    name = 'maps',
                    on_click = self.add_map,
                    max_active = 1,
                    element_color = (0, 0, 0, 0),
                    icon='map'
                ),
                Window([
                        Text((0.05, CONTROLS_GAP1), (0.2, 0.1), text = "bot1:", background_color = GUI_COLORS['blocked']),
                        Text(
                            (0.3, CONTROLS_GAP1), (0.65, 0.1),
                            text = "none", id='bot1',
                            background_color = GUI_COLORS['blocked'],
                            text_color = GUI_COLORS['button']
                        ),
                        
                        Text((0.05, CONTROLS_GAP1 * 2 + 0.1), (0.2, 0.1), text = "bot2:", background_color = GUI_COLORS['blocked']),
                        Text(
                            (0.3, CONTROLS_GAP1 * 2 + 0.1), (0.65, 0.1), 
                            text = "none", id='bot2', 
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

                        Text((0.05, CONTROLS_GAP1 * 4 + 0.3), (0.5, 0.1), text = "number of simulations:", background_color = GUI_COLORS['blocked']),
                        NumberField(
                            (0.6, CONTROLS_GAP1 * 4 + 0.3), (0.35, 0.1),
                            id='number_of_games',
                            minimum = 1,
                            maximum = 100,
                            default = 1,
                        ),

                        Text((0.05, CONTROLS_GAP1 * 5 + 0.4), (0.5, 0.1), text = "max ready timeout [s]:", background_color = GUI_COLORS['blocked']),
                        NumberField(
                            (0.6, CONTROLS_GAP1 * 5 + 0.4), (0.35, 0.1),
                            id='ready_timeout',
                            minimum = 1,
                            maximum = 100,
                            default = 10,
                        ),

                        Text((0.05, CONTROLS_GAP1 * 6 + 0.5), (0.5, 0.1), text = "max move timeout [s]:", background_color = GUI_COLORS['blocked']),
                        NumberField(
                            (0.6, CONTROLS_GAP1 * 6 + 0.5), (0.35, 0.1),
                            id='move_timeout',
                            minimum = 1,
                            maximum = 100,
                            default = 10,
                        ),

                        Text((0.05, CONTROLS_GAP1 * 7 + 0.6), (0.5, 0.1), text = "max game timeout [s]:", background_color = GUI_COLORS['blocked']),
                        NumberField(
                            (0.6, CONTROLS_GAP1 * 7 + 0.6), (0.35, 0.1),
                            id='game_timeout',
                            minimum = 1,
                            maximum = 100,
                            default = 60,
                        ),
                        InputField(
                            (0.05, CONTROLS_GAP1 * 8 + 0.7), (0.5, 0.1), 
                            default = "enter log name...", 
                            background_color = GUI_COLORS['blocked'],
                            text_color = GUI_COLORS['button'],
                            id = 'log_name_input',
                            when_type = self.update_start_button
                        ),
                        Button(
                            (0.6, CONTROLS_GAP1 * 8 + 0.7), (0.35, 0.1),
                            on_click = self.run_simulation,
                            text = 'start simulation',
                            blocked = True,
                            id='start_simulation_button',
                        ),
                    ], 
                    (PROPORTION1, 0), (1 - PROPORTION1, PROPORTION2),
                    name = 'control',
                    icon = 'simulation'
                ),
                Window([
                        ProgressBar(
                            (0.05, CONTROLS_GAP2), (0.9, 0.1 / PROPORTION2),
                            id = 'progress_bar',
                        ),
                        Text((0.05, CONTROLS_GAP2 * 2 + 0.1 / PROPORTION2), (0.35, 0.1 / PROPORTION2), text = "bot1 won games:", background_color = GUI_COLORS['blocked']),
                        ProgressBar(
                            (0.42, CONTROLS_GAP2 * 2 + 0.1 / PROPORTION2), (0.36, 0.1 / PROPORTION2),
                            id = 'bot1_won_progress_bar',
                        ),
                        Text((0.8, CONTROLS_GAP2 * 2 + 0.1 / PROPORTION2), (0.15, 0.1 / PROPORTION2), text = "0", background_color = GUI_COLORS['blocked'], id='bot1_wins'),
                        Text((0.05, CONTROLS_GAP2 * 3 + 0.2 / PROPORTION2), (0.35, 0.1 / PROPORTION2), text = "bot2 won games:", background_color = GUI_COLORS['blocked']),
                        ProgressBar(
                            (0.42, CONTROLS_GAP2 * 3 + 0.2 / PROPORTION2), (0.36, 0.1 / PROPORTION2),
                            id = 'bot2_won_progress_bar',
                        ),
                        Text((0.8, CONTROLS_GAP2 * 3 + 0.2 / PROPORTION2), (0.15, 0.1 / PROPORTION2), text = "0", background_color = GUI_COLORS['blocked'], id='bot2_wins'),
                        Button(
                            (0.25, CONTROLS_GAP2 * 4 + 0.3 / PROPORTION2), (0.5, 0.1 / PROPORTION2),
                            on_click = scene_functions['game'],
                            text = 'open last simulation view',
                            args = (),
                            blocked = True,
                            id='start_view_button',
                        ),
                    ], 
                    (PROPORTION1, PROPORTION2), (1 - PROPORTION1, 1 - PROPORTION2),
                    name = 'progress',
                    icon = 'timer'
                ),
            ], 
        )
    
    def add_bot(self, active_buttons):
        if len(active_buttons) == 0:
            self.scene.send_info('bot1', 'text', "none")
            self.scene.send_info('bot1', 'text_color', GUI_COLORS['button'])
            self.scene.send_info('bot2', 'text', "none")
        elif len(active_buttons) == 1:
            self.scene.send_info('bot1', 'text', active_buttons[0])
            self.scene.send_info('bot2', 'text', "none")
            self.scene.send_info('bot2', 'text_color', GUI_COLORS['button'])
            self.scene.send_info('bot1', 'text_color', GUI_COLORS['active'])
        elif len(active_buttons) == 2:
            self.scene.send_info('bot1', 'text', active_buttons[0])
            self.scene.send_info('bot2', 'text', active_buttons[1])
            self.scene.send_info('bot2', 'text_color', GUI_COLORS['active'])
        self.update_start_button()

    def add_map(self, active_buttons):
        if len(active_buttons) == 0:
            self.scene.send_info('map', 'text', "none")
            self.scene.send_info('map', 'text_color', GUI_COLORS['button'])
        elif len(active_buttons) == 1:
            self.scene.send_info('map', 'text', active_buttons[0])
            self.scene.send_info('map', 'text_color', GUI_COLORS['active'])
        self.update_start_button()

    def set_progress_bar_state(self, bar_name, state):
        self.scene.send_info(bar_name, 'state', min(max(state, 0), 1))

    def run_simulation(self):
        bot1 = self.scene.get_info('bot1', 'text')
        bot2 = self.scene.get_info('bot2', 'text')
        map = self.scene.get_info('map', 'text')
        number_of_games = int(self.scene.get_info('number_of_games', 'text'))
        ready_timeout = int(self.scene.get_info('ready_timeout', 'text'))
        move_timeout = int(self.scene.get_info('move_timeout', 'text'))
        game_timeout = int(self.scene.get_info('game_timeout', 'text'))
        log_name = self.scene.get_info('log_name_input', 'text')

        self.progress = 0
        self.bot1_wins = 0
        self.bot2_wins = 0

        simulations = play(
            bot1, bot2, number_of_games, map, log_name, 
            ready_timeout, move_timeout, game_timeout
        )

        def run_thread():
            for result in simulations:
                self.progress += 1
                self.set_progress_bar_state(
                    'progress_bar', self.progress / number_of_games)
                if result == 0:
                    self.bot1_wins += 1
                    self.scene.send_info('bot1_wins', 'text', str(self.bot1_wins))
                    self.set_progress_bar_state(
                        'bot1_won_progress_bar', self.bot1_wins / number_of_games)
                elif result == 1:
                    self.bot2_wins += 1
                    self.scene.send_info('bot2_wins', 'text', str(self.bot2_wins))
                    self.set_progress_bar_state(
                        'bot2_won_progress_bar', self.bot2_wins / number_of_games)
            self.simulation_complete(log_name)
        
        thread = Thread(target = run_thread)
        thread.start()
    
    def update_start_button(self):
        bot1 = self.scene.get_info('bot1', 'text')
        bot2 = self.scene.get_info('bot2', 'text')
        map = self.scene.get_info('map', 'text')
        log_name = self.scene.get_info('log_name_input', 'text')
        self.scene.send_info('start_simulation_button', 'blocked', any((
            bot1 == "none",
            bot2 == "none",
            map == "none",
            " " in log_name
        )))

    def simulation_complete(self, log_name):
        self.scene.send_info('start_view_button', 'args', (log_name,)) 
        self.scene.send_info('start_view_button', 'blocked', False)


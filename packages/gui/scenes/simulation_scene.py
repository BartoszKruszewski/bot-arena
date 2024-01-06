from packages.gui.abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Scene, Button, Window, List, NumberField, Text, ProgressBar
from os import listdir
from packages import MAPS_DIRECTORY, BOTS_DIRECTORY
from packages.simulator.api import play
from threading import Thread

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
                        NumberField(
                            (0, 0), (0.3, 0.3),
                            name = 'number of simulations',
                            id='number_of_games',
                            minimum = 1,
                            maximum = 100,
                            default = 1,
                        ),
                        Text((0, 0.4), (1, 0.1), text = "empty bot1", font_size = 30, id='bot1'),
                        Text((0, 0.6), (1, 0.1), text = "empty bot2", font_size = 30, id='bot2'),
                        Text((0, 0.8), (1, 0.1), text = "empty map", font_size = 30, id='map'),
                        Button(
                            (0.3, 0.4), (0.4, 0.1),
                            color=(255, 255, 0),
                            on_click = self.run_simulation,
                            text = 'start simulation',
                            blocked = True,
                            id='start_simulation_button'
                        ),
                    ], 
                    (PROPORTION1, 0), (1 - PROPORTION1, PROPORTION2),
                    color=(42, 42, 42), name = 'control'
                ),
                Window([
                        ProgressBar((0, 0), (1, 0.2), id = 'progress_bar'),
                        Button(
                            (0.3, 0.4), (0.4, 0.1),
                            color=(255, 255, 0),
                            on_click=scene_functions['game'],
                            text = 'simulation view',
                            args = (),
                            blocked = True,
                            id='start_view_button'
                        ),
                    ], 
                    (PROPORTION1, PROPORTION2), (1 - PROPORTION1, 1 - PROPORTION2),
                    color=(126, 126, 126), name = 'progress'
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
        self.update_start_button()

    def add_map(self, active_buttons):
        if len(active_buttons) == 0:
            self.scene.send_info('map', 'text', 'empty map')
        elif len(active_buttons) == 1:
            self.scene.send_info('map', 'text', active_buttons[0])
        self.update_start_button()

    def set_progress_bar_state(self, state):
        self.scene.send_info('progress_bar', 'state', min(max(state, 0), 1))

    def run_simulation(self):
        bot1 = self.scene.get_info('bot1', 'text')
        bot2 = self.scene.get_info('bot2', 'text')
        map = self.scene.get_info('map', 'text')
        number_of_games = int(self.scene.get_info('number_of_games', 'text'))
        
        self.progress = 0

        def run_thread():
            play(bot1, bot2, 1, map)
            self.progress += 1
            self.set_progress_bar_state(self.progress / number_of_games)
            if self.progress < number_of_games:
                run_thread()
            else:
                # tu trzeba dac nazwe ostatniego loga zamiast "example_log"
                self.scene.send_info('start_view_button', 'args', ('example_log',)) 
                self.scene.send_info('start_view_button', 'blocked', False)

        thread = Thread(target = run_thread)
        thread.start()
    
    def update_start_button(self):
        bot1 = self.scene.get_info('bot1', 'text')
        bot2 = self.scene.get_info('bot2', 'text')
        map = self.scene.get_info('map', 'text')
        self.scene.send_info('start_simulation_button', 'blocked', any((
            bot1 == 'empty bot1',
            bot2 == 'empty bot2',
            map == 'empty map',
        )))
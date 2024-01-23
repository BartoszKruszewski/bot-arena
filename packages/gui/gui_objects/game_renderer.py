from pygame import MOUSEWHEEL, Surface, Vector2
from pygame.event import get as get_event

from packages.gui.gui_objects.gui_element import GUIElement
from packages.game_logic.game import Game
from packages.gui.game_render import LogInterpreter, Engine
from packages.gui.const import FRAMERATE, ZOOM_INTERWAL, \
    MIN_ZOOM, MAX_ZOOM, TILE_SIZE, MIN_GAME_SPEED, MAX_GAME_SPEED
from packages import LOGS_DIRECTORY
from os import listdir
from os import path

class GameRenderer(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        try:
            self.__log_interpreter = LogInterpreter(
                path.join(LOGS_DIRECTORY, self.properties.get("log_name", "log")) 
            )
        except FileNotFoundError:
            print('No log!')
        self.__game = Game(self.__log_interpreter.get_map_name())
        
        self.__engine = Engine(self.__game)
        
        self.__tick = 0
        self.__dt = 0
        
        self.__last_game_speed = 1

        self.properties['game_speed'] = 1
        self.properties['zoom'] = 1
        self.properties['set_zoom'] = self.set_zoom
        self.properties['set_game_speed'] = self.set_game_speed
        self.properties['toogle_freeze'] = self.toogle_freeze
        self.properties['log_index'] = self.__log_interpreter.get_index()
        self.properties['game_stats'] = {
            "gold": self.__game.get_gold(), 
            "income": self.__game.get_income()
        }
        self.properties['helpers'] = []

    def handle_event(self, event):
        if event.type == MOUSEWHEEL:
            if self.in_mouse_range():
                zoom = self.properties.get('zoom', 1)
                zoom += event.y * ZOOM_INTERWAL * zoom
                self.set_zoom(zoom)

    def set_zoom(self, value):
        self.properties['zoom'] = max(
            self.real_size.x / self.__game.get_map_size()[0] / TILE_SIZE,
            self.real_size.y / self.__game.get_map_size()[1] / TILE_SIZE,
            min(MAX_ZOOM, value),
            MIN_ZOOM
        )

    def set_game_speed(self, value):
        self.properties['game_speed'] = max(
            min(MAX_GAME_SPEED, value),
            MIN_GAME_SPEED
        )

    def toogle_freeze(self):
        if self.properties['game_speed'] == 0:
            self.properties['game_speed'] = self.__last_game_speed
        else:
            self.properties['game_speed'] = 0

    def update(self, dt):
        self.__tick += dt * self.properties.get('game_speed', 1)

        if self.__tick > FRAMERATE:
            game_output = self.__game.update(*self.__log_interpreter.get_next_actions())
            if 'win' in game_output[0]:
                self.properties.get('game_end_action', lambda: None)() 
            self.__tick %= FRAMERATE
    
        self.__dt = dt
        self.properties['log_index'] = self.__log_interpreter.get_index()
        self.properties['game_stats'] = {
            "gold": self.__game.get_gold(), 
            "income": self.__game.get_income()
        }

    def render(self) -> Surface:
        return self.__engine.render(
            self.__game,
            self.__dt,
            Vector2(self.real_size.x, int(self.real_size.y)),
            self.global_pos,
            self.properties.get('zoom', 1),
            self.properties.get('game_speed', 1),
            self.properties.get('helpers', []))

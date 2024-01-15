from pygame import MOUSEWHEEL, Surface, Vector2
from pygame.event import get as get_event

from packages.gui.gui_objects.gui_element import GUIElement
from packages.game_logic.game import Game
from packages.gui.game_render import LogInterpreter, Engine
from packages.gui.const import FRAMERATE, ZOOM_INTERWAL, \
    MIN_ZOOM, MAX_ZOOM, TILE_SIZE
from packages import LOGS_DIRECTORY
from os import listdir

class GameRenderer(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        log_name = self.properties.get('log_name', 'log')
        file_name = listdir(f'{LOGS_DIRECTORY}/{log_name}')[-1]
        try:
            self.__log_interpreter = LogInterpreter(
                f'{LOGS_DIRECTORY}/{log_name}/{file_name}'
            )
        except FileNotFoundError:
            print('No log!')
        self.__game = Game(self.__log_interpreter.get_map_name())
        
        self.__engine = Engine(self.__game)
        
        self.__tick = 0
        self.__dt = 0
        
        self.properties['game_speed'] = 1
        self.properties['zoom'] = 1
        self.properties['log_index'] = self.__log_interpreter.get_index()
        self.properties['game_stats'] = {
            "gold": self.__game.get_gold(), 
            "income": self.__game.get_income()
        }
        self.properties['helpers'] = []

    def __update_zoom(self):
        zoom = self.properties.get('zoom', 1)

        if self.in_mouse_range():
            e = get_event(MOUSEWHEEL)
            if e:
                zoom += e[0].y * ZOOM_INTERWAL * zoom

        zoom = max(
            self.real_size.x / self.__game.get_map_size()[0] / TILE_SIZE,
            self.real_size.y / self.__game.get_map_size()[1] / TILE_SIZE,
            min(MAX_ZOOM, zoom),
            MIN_ZOOM
        )

        self.properties['zoom'] = zoom

    def update(self, dt):
        self.__tick += dt * self.properties.get('game_speed', 1)

        if self.__tick > FRAMERATE:
            game_output = self.__game.update(*self.__log_interpreter.get_next_actions())
            if 'win' in game_output[0]:
                self.properties.get('game_end_action', lambda: None)() 
            self.__tick %= FRAMERATE
        
        self.__update_zoom()
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

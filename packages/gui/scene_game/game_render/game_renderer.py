from pygame import init, WINDOWCLOSE, Vector2, Surface
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.time import Clock
from pygame.event import peek as event_peek
from os import name as os_name

from ....game_logic.game import Game

from .log_interpreter import LogInterpreter
from .engine import Engine

from ...pygame_tree.gui_object import Window, GUIElement
from ...mouse import Mouse
from ...const import SCREEN_SIZE, FRAMERATE
from ...const import ZOOM_INTERWAL, MIN_ZOOM, MAX_ZOOM, TILE_SIZE

from packages import MAPS_DIRECTORY

class GameRender(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        super().__init__(pos, size)
        self.__game = Game()
        self.__log_interpreter = LogInterpreter("./logs/" + 'example_log.txt')
        self.__engine = Engine(self.__game)
        self.__zoom = 1
        self.__tick = 0  
    
    def set_zoom(self, value):
        min_zoom = max(
            self.real_size.x / self.__game.get_map_size()[0] / TILE_SIZE,
            self.real_size.y / self.__game.get_map_size()[1] / TILE_SIZE,
            MIN_ZOOM
        )
        self.__zoom = max(min_zoom, min(MAX_ZOOM, value))

    def render(self, dt: float, mouse: Mouse) -> Surface:
        self.set_zoom(self.__zoom)
        # if self.in_mouse_range(mouse):
        #     self.set_zoom(self.__zoom + mouse.wheel * ZOOM_INTERWAL * self.__zoom)

        self.__tick += dt
        if self.__tick > FRAMERATE:
            game_output = self.__game.update(*self.__log_interpreter.get_next_actions())
            self.__tick = 0

        return self.__engine.render(
                self.__game, dt, self.real_size, mouse,
                self.global_pos, self.__zoom, 1)

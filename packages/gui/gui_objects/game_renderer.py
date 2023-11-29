from pygame import MOUSEWHEEL, Surface
from pygame.event import get as get_event

from packages.gui.gui_objects.gui_element import GUIElement
from packages.game_logic.game import Game
from packages.gui.game_render.log_interpreter import LogInterpreter
from packages.gui.game_render.engine import Engine
from packages.gui.const import FRAMERATE, ZOOM_INTERWAL, \
    MIN_ZOOM, MAX_ZOOM, TILE_SIZE

class GameRenderer(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size)
        self.__game = Game()
        self.__log_interpreter = LogInterpreter("./logs/" + 'example_log.txt')
        self.__engine = Engine(self.__game)
        self.__zoom = 1
        self.__tick = 0
        self.__dt = 0

    def update(self, dt):
        self.__tick += dt
        if self.__tick > FRAMERATE:
            game_output = self.__game.update(*self.__log_interpreter.get_next_actions())
            self.__tick %= FRAMERATE
        
        if self.in_mouse_range():
            e = get_event(MOUSEWHEEL)
            if e:
                self.__zoom += e[0].y * ZOOM_INTERWAL * self.__zoom

        self.__zoom = max(
            self.real_size.x / self.__game.get_map_size()[0] / TILE_SIZE,
            self.real_size.y / self.__game.get_map_size()[1] / TILE_SIZE,
            min(MAX_ZOOM, self.__zoom),
            MIN_ZOOM
        )

        self.__dt = dt

    def render(self) -> Surface:
        return self.__engine.render(
            self.__game, self.__dt, self.real_size, self.global_pos, self.__zoom, 1)

from pygame import init, WINDOWCLOSE, Vector2, Surface
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.event import peek as event_peek

from ..gui_object import Window, GUIElement, InputField
from ..gui_object import RectButton, SquareButton, GoBackButton
from ..mouse import Mouse
from ..const import SCREEN_SIZE

from packages import MAPS_DIRECTORY

from time import sleep

class Main:
    def __init__(self):
        self.__screen = display_set_mode(SCREEN_SIZE)
        self.__is_running = True
        self.__mouse = Mouse()
        self.__dt = 1

        self.__gui = None
        self.last_info = {}
        
        self.__set_size_scene()
        
        while self.__is_running:
            self.__mouse.update()
            self.__is_running = not event_peek(WINDOWCLOSE)
            self.__screen_update()

    def __stop(self):
        self.__is_running = False

    def submit_size(self):
        self.__gui.collect_info(self.last_info)
        print(self.last_info)
        ERROR = ""
        
        map_x_size = self.last_info['map_x_size']
        map_y_size = self.last_info['map_y_size']
        if not map_x_size.isdigit() or not map_y_size.isdigit():
            ERROR = "Not number"
        elif int(map_x_size) <= 3 or int(map_y_size) <= 3:
            ERROR += "Input numbers > 3"
        elif int(map_x_size) > 25 or int(map_y_size) > 25:
            ERROR += "Input numbers <= 25"

        if ERROR != "":
            self.__set_size_scene(ERROR)
        else:
            self.__set_generate_scene()

    def __set_size_scene(self, ERROR : str = "") -> None:
        sleep(0.5)

        self.__gui =  Window([
            RectButton(
                (0.1, 0.1), (0.8, 0.1),
                color=(255, 0, 0) if ERROR != "" else (0, 0, 0), 
                text=ERROR,
                ),
            InputField((0.2, 0.4), (0.3, 0.1), placeholder="Map X size", collect_info='map_x_size'),
            InputField((0.5, 0.4), (0.3, 0.1), placeholder="Map Y size", collect_info='map_y_size'),
            RectButton(
                (0.4, 0.6), (0.2, 0.1), 
                text="Submit", 
                color=(50,205,50),
                on_click=self.submit_size
                ),
            GoBackButton(on_click=self.__stop)
        ], (0, 0), (1, 1))

        self.__gui.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def __set_generate_scene(self) -> None:
        sleep(0.5)

        self.__gui = Window([
            RectButton(
                (0.4, 0.6), (0.2, 0.1), 
                text="Generate", 
                color=(50,205,50),
                ),
            GoBackButton(on_click=self.__stop)
        ], (0, 0), (1, 1))

        self.__gui.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def __screen_update(self):
        '''Refreshes screen and update frame clock.
        '''
        self.__screen.blit(self.__gui.get_surface(self.__dt, self.__mouse), (0, 0))
        display_update()

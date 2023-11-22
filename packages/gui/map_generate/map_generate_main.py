from pygame import init, WINDOWCLOSE, Vector2, Surface
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.event import peek as event_peek

from ..gui_object import Window, InputField
from ..gui_object import RectButton, GoBackButton, SubmitButton, ErrorWindow
from ..mouse import Mouse
from ..const import SCREEN_SIZE

from packages import MAPS_DIRECTORY

from time import sleep

import json

class Main:
    def __init__(self):
        self.__screen = display_set_mode(SCREEN_SIZE)
        self.__is_running = True
        self.__mouse = Mouse()
        self.__dt = 1

        self.__gui = None
        self.last_info = {}
        
        self.__set_size_scene()
        
        self.path = []
        self.obstacles = []
        self.map_x_size = 0
        self.map_y_size = 0

        while self.__is_running:
            self.__mouse.update()
            self.__is_running = not event_peek(WINDOWCLOSE)
            self.__screen_update()

    def __stop(self):
        self.__is_running = False

    def submit_size(self):
        self.__gui.collect_info(self.last_info)
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
            self.__gui = ErrorWindow(ERROR, on_click=self.__set_size_scene)
        else:
            self.map_x_size = int(map_x_size)
            self.map_y_size = int(map_y_size)
            self.__set_path_scene()

    def __set_size_scene(self) -> None:
        sleep(0.5)

        self.__gui =  Window([
            InputField(
                (0.2, 0.4), (0.3, 0.1), 
                placeholder="Map X size", 
                collect_info='map_x_size',
                color=(0,0,128),
                on_click_color=(128, 0, 0),
                ),     
            InputField(
                (0.5, 0.4), (0.3, 0.1), 
                placeholder="Map Y size", 
                collect_info='map_y_size',
                color=(0,0,128),
                on_click_color=(128, 0, 0),
                ),
            SubmitButton(on_click=self.submit_size),
            GoBackButton(on_click=self.__stop)
        ], (0, 0), (1, 1))

        self.__gui.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def submit_path(self):
        path = []
        for object in self.__gui:
            if type(object) is not RectButton: continue   
            if object.is_clicked and object.properties.get('map_cords', None) is not None:
                path.append(object.properties['map_cords'])

        def neighbors(cords):
            x, y = cords
            return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

        for i, cords in enumerate(path):
            if i == 0 or i == len(path) - 1: continue
            count = 0
            for neighbor in neighbors(cords):
                if neighbor in path:
                    count += 1
            if count != 2:
                self.__gui = ErrorWindow("Path is not correct", on_click=self.__set_path_scene)
                return
        path.append((self.map_x_size - 1, self.map_y_size - 1))
        
        self.path = [(0, 0)]
        while path != []:
            for neighbor in neighbors(self.path[-1]):
                if neighbor in path:
                    self.path.append(neighbor)
                    path.remove(neighbor)
                    break

        self.__set_obstacles_scene()
            
    def __set_path_scene(self) -> None:
        sleep(0.5)

        start = Vector2(0.01, 0.1)
        map_x_size = self.map_x_size
        map_y_size = self.map_y_size
        size_x = 0.95 / map_x_size
        size_y = 0.75 / map_y_size

        buttons = []
        for x in range(map_x_size):
            for y in range(map_y_size):
                if (x == 0 and y == 0) or (x == map_x_size - 1 and y == map_y_size - 1):
                    buttons.append(RectButton(
                        (start.x + x * size_x, start.y + y * size_y), 
                        (size_x-0.01, size_y-0.01),
                        color=(255, 0, 0),
                        map_cords=(x, y)
                    ))
                else:
                    buttons.append(RectButton(
                        (start.x + x * size_x, start.y + y * size_y), 
                        (size_x-0.01, size_y-0.01),
                        color=(50, 50, 50),
                        on_click_color=(255, 128, 255),
                        map_cords=(x, y)
                    ))

        self.__gui = Window(buttons + [
            GoBackButton(on_click=self.__set_size_scene),
            SubmitButton(on_click=self.submit_path),

        ], (0, 0), (1, 1))
        
        self.__gui.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def submit_obstacles(self):
        self.obstacles = []
        for object in self.__gui:
            if type(object) is not RectButton: continue   
            if object.is_clicked and object.properties.get('map_cords', None) is not None:
                if object.properties['map_cords'] not in self.path:
                    self.obstacles.append(object.properties['map_cords'])
        
        self.__set_verify_scene()

    def __set_obstacles_scene(self) -> None:
        sleep(0.5)

        start = Vector2(0.01, 0.1)
        map_x_size = self.map_x_size
        map_y_size = self.map_y_size
        size_x = 0.95 / map_x_size
        size_y = 0.75 / map_y_size

        buttons = []
        for x in range(map_x_size):
            for y in range(map_y_size):
                if (x, y) in self.path:
                    buttons.append(RectButton(
                        (start.x + x * size_x, start.y + y * size_y), 
                        (size_x-0.01, size_y-0.01),
                        color=(255, 0, 0),
                        map_cords=(x, y)
                    ))
                else:
                    buttons.append(RectButton(
                        (start.x + x * size_x, start.y + y * size_y), 
                        (size_x-0.01, size_y-0.01),
                        color=(50, 50, 50),
                        on_click_color=(30, 50, 255),
                        map_cords=(x, y)
                    ))

        self.__gui = Window(buttons + [
            GoBackButton(on_click=self.__set_path_scene),
            SubmitButton(on_click=self.submit_obstacles),
        ], (0, 0), (1, 1))

        self.__gui.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def __set_verify_scene(self) -> None:
        sleep(0.5)

        buttons = []

        for object in self.__gui:
            if object.properties.get('map_cords', None) is not None:
                new_button = RectButton(
                    object.pos, object.size, 
                    color=object.properties.get('color') if object.properties.get('color') != (50, 50, 50) else (90, 90, 90),
                )
                buttons.append(new_button)
                
        self.__gui = Window(buttons + [
            GoBackButton(on_click=self.__set_obstacles_scene),
            SubmitButton(on_click=self.save_map),
        ], (0, 0), (1, 1))

        self.__gui.calc_pos(Vector2(SCREEN_SIZE), Vector2(0, 0))

    def __screen_update(self):
        '''Refreshes screen and update frame clock.
        '''
        self.__screen.blit(self.__gui.get_surface(self.__dt, self.__mouse), (0, 0))
        display_update()

    def save_map(self):
        map = {
            'path': self.path,
            'obstacles': self.obstacles,
            'MAP_SIZE_X': self.map_x_size,
            'MAP_SIZE_Y': self.map_y_size
        }
        print(MAPS_DIRECTORY + '\map.json')
        with open(MAPS_DIRECTORY + '\map.json', 'w') as file:
            json.dump(map, file, indent=4)

        self.__stop()

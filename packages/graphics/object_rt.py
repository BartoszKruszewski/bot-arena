from pygame import Vector2
from .const import TILE_SIZE, FRAMERATE, ANIMATION_SPEED, ANIMATION_LEN, MOUSE_TARGET_RADIUS

class ObjectRT():
    '''Real time object class used in graphics rendering.
    '''

    def __init__(self, cords: Vector2, id: int, name: str, side: str):

        # data
        self.cords = cords * TILE_SIZE
        self.id = id
        self.name = name
        self.side = side

        # state
        self.frame = 0
        self.tick = 0
        self.state = 'idle'
        self.select_time = 0

    def update(self, game_speed: float, mouse_pos: Vector2): 
        '''Main update function.

        Refreshes once per frame.
        '''

        if self.state != 'idle':
            self.__update_frame(game_speed)

        self.__update_select_time(mouse_pos)

    def __update_frame(self, game_speed: float):
        '''Updates actual animation frame.
        '''

        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED / game_speed:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0

    def __update_select_time(self, mouse_pos: Vector2):
        if mouse_pos.distance_to(self.cords) < MOUSE_TARGET_RADIUS:
            self.select_time += 1
        else:
            self.select_time = 0
        
from pygame import Vector2
from .const import TILE_SIZE, ROUND_LEN, FRAMERATE, ANIMATION_NAMES, ANIMATION_SPEED, ANIMATION_LEN
from .const import TILE_SIZE

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

    def update(self, game_speed: float): 
        '''Main update function.

        Refreshes once per frame.
        '''

        if self.state != 'idle':
            self.__update_frame(game_speed)

    def __update_frame(self, game_speed: float):
        '''Updates actual animation frame.
        '''

        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED / game_speed:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0

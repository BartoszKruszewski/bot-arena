from pygame import Vector2
from .const import TILE_SIZE, ROUND_LEN, FRAMERATE, ANIMATION_NAMES, ANIMATION_SPEED, ANIMATION_LEN
from .const import TILE_SIZE

class TurretRT():
    '''Real time turret class used in graphics rendering.
    '''

    def __init__(self, cords: Vector2, id: int) -> None:

        # data
        self.cords = cords * TILE_SIZE
        self.id = id

        # state
        self.frame = 0
        self.tick = 0

    def update(self):
        '''Main update function.

        Refreshes once per frame.
        '''

        self.__update_frame()

    def __update_frame(self):
        '''Updates actual animation frame.
        '''

        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0
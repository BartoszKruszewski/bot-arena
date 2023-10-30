from pygame import Vector2
from abc import ABC
from .const import FRAMERATE, ANIMATION_SPEED, ANIMATION_LEN, TILE_SIZE
from ..game_logic.stats import ROUND_LEN

class AnimatedObject(ABC):
    def __init__(self):
        self.frame = 0
        self.tick = 0
        self.direction = None
        self.animation = None
        self.pos = Vector2(0, 0)
        self.next_pos = Vector2(0, 0)
        self.real_pos = Vector2(0, 0)
        self.type = None
        self.name = None
        self.offset = Vector2(0, 0)

    def update(self):
        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0

        self.__update_direction()
        self.__update_real_pos()

    def __update_direction(self):
        diff = tuple(self.next_pos - self.pos)
        self.direction = {
            (0, -1):    'top',
            (0, 1):     'bot',
            (1, 0):     'left',
            (-1, 0):    'right'
        }[diff]

    def __update_real_pos(self):
        self.real_pos += (self.next_pos - self.pos) * TILE_SIZE * ROUND_LEN / FRAMERATE / 1000 

    
        
from pygame import Vector2
from abc import ABC
from .const import FRAMERATE, ANIMATION_SPEED, ANIMATION_LEN, TILE_SIZE


class AnimatedObject(ABC):
    def __init__(self):
        self.frame = 0
        self.tick = 0
        self.direction = 'bot'
        self.animation = None
        self.pos = Vector2(0, 0)
        self.type = None
        self.name = None
        self.offset = Vector2(0, 0)
        self.id = 0

    def update(self):
        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0

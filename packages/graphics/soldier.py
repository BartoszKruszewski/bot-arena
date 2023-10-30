from pygame import Vector2
from .animated_object import AnimatedObject
from .const import SPRITE_SIZE

class SoldierAnimatedObject(AnimatedObject):
    def __init__(self, pos, name):
        self.frame = 0
        self.direction = 'bot'
        self.animation = 'walk'
        self.pos = Vector2(0, 0)
        self.type = 'soldiers'
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)

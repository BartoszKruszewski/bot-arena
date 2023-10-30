from pygame import Vector2
from abc import ABC

class AnimatedObject(ABC):
    def __init__(self):
        self.frame = 0
        self.direction = None
        self.animation = None
        self.pos = Vector2(0, 0)
        self.type = None
        self.name = None
        self.offset = Vector2(0, 0)
from pygame import Vector2
from .animated_object import AnimatedObject
from .const import SPRITE_SIZE

class SoldierAnimatedObject(AnimatedObject):
    def __init__(self, pos, name):
        self.frame = 0
        self.tick = 0
        self.direction = 'bot'
        self.animation = 'walk'
        self.pos = pos
        self.type = 'soldiers'
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)

    def update_next_pos(self, path):
        pos = self.pos.x, self.pos.y
        i = 0
        while i < len(path) or path[i] != pos:
            i += 1
        
        self.next_pos = Vector2(path[i + 1])

    

    
        

from pygame import Vector2
from .animated_object import AnimatedObject
from .const import SPRITE_SIZE
from .soldier import Soldier

class SoldierAnimatedObject(Soldier, AnimatedObject):
    def __init__(self, pos, name):
        self.animation = 'walk'
        self.pos = pos
        self.type = 'soldiers'
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)

    def update(self):
        super().update()
        self.__update_real_pos()
        self.__update_direction()

    def __update_direction(self):
        diff = tuple(self.next_pos - self.pos)
        self.direction = {
            (0, -1):    'top',
            (0, 1):     'bot',
            (1, 0):     'left',
            (-1, 0):    'right'
        }[diff]
        

    

    

    
        

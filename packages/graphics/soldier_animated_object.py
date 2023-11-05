from pygame import Vector2
from .animated_object import AnimatedObject
from .const import SPRITE_SIZE, TILE_SIZE, ROUND_LEN, FRAMERATE, ANIMATION_NAMES

class SoldierAnimatedObject(AnimatedObject):
    path = []

    def __init__(self, id: int, path_pos: int, name: str, side: str):
        super().__init__(id)
        self.animation = 'walk'
        self.type = 'soldiers'
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)
        self.path_pos = path_pos
        self.side = side
        self.real_pos = SoldierAnimatedObject.path[path_pos]
        self.direction_v = Vector2(0, 0)

    def update(self):
        super().update()
        self.__update_direction()
        self.__update_real_pos()

    def set_path_position(self, pos: int):
        if self.path_pos != pos:
            self.path_pos = pos
            self.real_pos = Vector2(SoldierAnimatedObject.path[self.path_pos]) * TILE_SIZE + Vector2(TILE_SIZE // 2, TILE_SIZE // 2)

    def set_animation(self, animation: str):
        if self.animation not in ANIMATION_NAMES:
            raise Exception('Animation not exists!')
        if animation != self.animation:
            self.frame = 0
            self.animation = animation
        
    def __update_direction(self):
        if self.side == 'left':
            self.direction_v = Vector2(SoldierAnimatedObject.path[self.path_pos + 1]) - Vector2(SoldierAnimatedObject.path[self.path_pos])
        else:
            self.direction_v = Vector2(SoldierAnimatedObject.path[self.path_pos - 1]) - Vector2(SoldierAnimatedObject.path[self.path_pos])

        self.direction = {
            (0, -1):    'top',
            (0, 1):     'bot',
            (-1, 0):     'left',
            (1, 0):    'right'
        }[(int(self.direction_v.x), int(self.direction_v.y))]

    def __update_real_pos(self):
        if self.animation == 'walk':
            self.real_pos += self.direction_v * TILE_SIZE * 1000 / ROUND_LEN / FRAMERATE
            
        elif self.animation == 'fight':
            self.real_pos = Vector2(SoldierAnimatedObject.path[self.path_pos + (-1 if self.side == "left" else 1)]) * TILE_SIZE + Vector2(TILE_SIZE // 2, TILE_SIZE // 2)

    def __str__(self):
        return f'<{self.side}:{self.id} {self.real_pos}>'
        

    

    

    
        

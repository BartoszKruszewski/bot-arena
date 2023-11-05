from pygame import Vector2
from .animated_object import AnimatedObject
from .const import SPRITE_SIZE, TILE_SIZE, ROUND_LEN, FRAMERATE

class SoldierAnimatedObject(AnimatedObject):
    def __init__(self, path_pos, real_pos, name, side):
        super().__init__()
        self.animation = 'walk'
        self.type = 'soldiers'
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)
        self.path_pos = path_pos
        self.side = side
        self.real_pos = real_pos
        self.direction_v = Vector2(0, 0)

    def update(self, path: list[tuple[int, int]]):
        super().update()
        self.__update_direction(path)
        self.__update_real_pos()

    def set_path_position(self, pos):
        self.path_pos = pos
        

    def set_animation(self, animation: str):
        self.animation = animation

    def __update_direction(self, path: list[tuple[int, int]]):
        if self.side == 'left':
            self.direction_v = Vector2(path[self.path_pos + 1]) - Vector2(path[self.path_pos])
        else:
            self.direction_v = Vector2(path[self.path_pos - 1]) - Vector2(path[self.path_pos])

        self.direction = {
            (0, -1):    'top',
            (0, 1):     'bot',
            (-1, 0):     'left',
            (1, 0):    'right'
        }[(int(self.direction_v.x), int(self.direction_v.y))]

    def __update_real_pos(self):
        if self.animation == 'walk':
            self.real_pos += self.direction_v * TILE_SIZE * 1000 / ROUND_LEN / FRAMERATE 

    def __str__(self):
        return f'<{self.side}:{self.id} {self.real_pos}>'
        

    

    

    
        

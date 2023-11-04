from pygame import Vector2
from .animated_object import AnimatedObject
from .const import SPRITE_SIZE, TILE_SIZE, ROUND_LEN, FRAMERATE

class SoldierAnimatedObject(AnimatedObject):
    def __init__(self, pos, name, side):
        super().__init__()
        self.animation = 'walk'
        self.type = 'soldiers'
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)
        self.path_pos = pos
        self.side = side
        self.real_pos = Vector2(0.0, 0.0)
        self.direction_v = Vector2(0, 0)

    def update(self, path: list[tuple[int, int]]):
        super().update()
        self.__update_direction(path)
        self.__update_real_pos()

    def set_path_position(self, pos):
        self.path_pos = pos

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
        self.real_pos += self.direction_v * TILE_SIZE * ROUND_LEN / FRAMERATE / 1000
        

    

    

    
        

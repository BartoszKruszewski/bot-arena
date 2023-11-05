from pygame import Vector2
from .const import SPRITE_SIZE, TILE_SIZE, ROUND_LEN, FRAMERATE, ANIMATION_NAMES, ANIMATION_SPEED, ANIMATION_LEN

class SoldierRT():
    path = []

    def __init__(self, id: int, path_pos: int, name: str, side: str):
        # state
        self.id = id
        self.frame = 0
        self.tick = 0
        self.direction = 'bot'
        self.direction_v = Vector2(0, 0)
        self.animation = 'walk'
        self.state = 'walk'
        self.real_pos = SoldierRT.path[path_pos]
        self.path_pos = path_pos

        # data    
        self.name = name
        self.offset = Vector2(SPRITE_SIZE // 2, SPRITE_SIZE // 2)
        self.side = side

    def update(self):
        self.__update_frame()
        self.__update_direction()
        self.__update_real_pos()
        self.__update_animation()

    def set_path_position(self, pos: int):
        if self.path_pos != pos:
            self.path_pos = pos
            self.real_pos = Vector2(SoldierRT.path[self.path_pos]) * TILE_SIZE + Vector2(TILE_SIZE // 2, TILE_SIZE // 2)

    def set_state(self, state: str):
        if state not in ANIMATION_NAMES and state != 'idle':
            raise Exception('Animation not exists!')
        self.state = state

    def __update_animation(self):
        if self.state == 'fight':
            self.animation = 'fight'
        else:
            self.animation = 'walk'

    def __update_direction(self):
        if self.side == 'left':
            self.direction_v = Vector2(SoldierRT.path[self.path_pos + 1]) \
                - Vector2(SoldierRT.path[self.path_pos])
        else:
            self.direction_v = Vector2(SoldierRT.path[self.path_pos - 1]) \
                - Vector2(SoldierRT.path[self.path_pos])

        self.direction = {
            (0, -1):    'top',
            (0, 1):     'bot',
            (-1, 0):     'left',
            (1, 0):    'right'
        }[(int(self.direction_v.x), int(self.direction_v.y))]

    def __update_real_pos(self):
        if self.state == 'walk':
            self.real_pos += self.direction_v * TILE_SIZE * 1000 / ROUND_LEN / FRAMERATE
        else:
            self.real_pos = Vector2(SoldierRT.path[self.path_pos]) \
                * TILE_SIZE + Vector2(TILE_SIZE // 2, TILE_SIZE // 2)

    def __update_frame(self):
        if not self.state == 'idle':
            self.tick += 1
            if self.tick > FRAMERATE // ANIMATION_SPEED:
                self.tick = 0
                self.frame += 1
                if self.frame >= ANIMATION_LEN:
                    self.frame = 0

    def __str__(self):
        return f'<{self.side}:{self.id} {self.real_pos}>'
    

        

    

    

    
        

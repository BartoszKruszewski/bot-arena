from pygame import Vector2
from .const import TILE_SIZE, ROUND_LEN, FRAMERATE, ANIMATION_NAMES, ANIMATION_SPEED, ANIMATION_LEN

class SoldierRT():
    '''Real time soldier graphics class.
    '''

    path = [] 

    def __init__(self, id: int, path_pos: int, name: str, side: str):

        # data
        self.id = id
        self.name = name
        self.side = side

        # state
        self.frame = 0
        self.tick = 0
        self.direction = Vector2(0, 0)
        self.animation = 'walk'
        self.state = 'walk'
        self.real_pos = Vector2(SoldierRT.path[path_pos]) * TILE_SIZE
        self.path_pos = path_pos

    def update(self):
        '''Main update function.

        Refreshes once per frame.
        '''

        self.__update_frame()
        self.__update_direction()
        self.__update_real_pos()
        self.__update_animation()

    def set_path_position(self, pos: int):
        '''Soldier in path position setter.

        Path position is id of path element
        (from 0 to path lenght).
        '''

        if pos < 0 or pos > len(SoldierRT.path):
            raise Exception('Position not in path!')
        if (self.side == "left" and pos < self.path_pos) or \
            (self.side == "right" and pos > self.path_pos):
            raise Exception('Soldier cannot move back!')
        if self.path_pos != pos:
            self.path_pos = pos
            self.real_pos = Vector2(SoldierRT.path[self.path_pos]) * TILE_SIZE

    def set_state(self, state: str):
        '''Soldier state setter.

        States:
            - idle (no moving, stay in place, no animation)
            - walk (moving by the path, walking animation)
            - fight (no moving, fight animation)
        '''

        if state not in ANIMATION_NAMES and state != 'idle':
            raise Exception('Animation not exists!')
        self.state = state

    def __update_animation(self):
        '''Updates actual animation name.
        '''

        if self.state == 'fight':
            self.animation = 'fight'
        else:
            self.animation = 'walk'

    def __update_direction(self):
        '''Updates actual direction vector.
        '''

        if self.side == 'left':
            self.direction = Vector2(SoldierRT.path[self.path_pos + 1]) \
                - Vector2(SoldierRT.path[self.path_pos])
        else:
            self.direction = Vector2(SoldierRT.path[self.path_pos - 1]) \
                - Vector2(SoldierRT.path[self.path_pos])

    def __update_real_pos(self):
        '''Updates actual real position.

        Position is in float px value.
        '''
        if self.state == 'walk':
            self.real_pos += self.direction * TILE_SIZE * 1000 / ROUND_LEN / FRAMERATE
        else:
            self.real_pos = Vector2(SoldierRT.path[self.path_pos]) * TILE_SIZE

    def __update_frame(self):
        '''Updates actual animation frame.
        '''

        if not self.state == 'idle':
            self.tick += 1
            if self.tick > FRAMERATE // ANIMATION_SPEED:
                self.tick = 0
                self.frame += 1
                if self.frame >= ANIMATION_LEN:
                    self.frame = 0

    def __str__(self):
        return f'<{self.side}:{self.id} {self.real_pos}>'
    

        

    

    

    
        

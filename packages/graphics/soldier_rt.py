from pygame import Vector2
from .const import TILE_SIZE, FRAMERATE, ANIMATION_NAMES, ANIMATION_SPEED, ANIMATION_LEN, HP_BAR_SMOOTH
from .object_rt import ObjectRT

class SoldierRT(ObjectRT):
    '''Real time soldier graphics class.
    '''

    path = [] 

    def __init__(self, id: int, path_pos: int, name: str, side: str, stats: dict):
        
        super().__init__(Vector2(SoldierRT.path[path_pos]), id, name, side, stats)

        # data
        self.actual_hp_rate = 1

        # state
        self.direction = Vector2(0, 0)
        self.animation = 'walk'
        self.cords = Vector2(SoldierRT.path[path_pos]) * TILE_SIZE
        self.path_pos = path_pos
        self.actual_hp = self.stats['max_hp']

    def update(self, game_speed: float, mouse_pos: Vector2):
        '''Main update function.

        Refreshes once per frame.
        '''

        super().update(game_speed, mouse_pos)
        self.__update_direction()
        self.__update_cords(game_speed)
        self.__update_animation()
        self.__update_hp_rate()
        
    def set_hp(self, value):
        if value > self.stats['max_hp'] or value < 0:
            raise Exception('Invalid HP value!')
        self.actual_hp = value

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
            self.cords = Vector2(SoldierRT.path[self.path_pos]) * TILE_SIZE

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
            if self.path_pos == len(SoldierRT.path) - 1: return
                
            self.direction = Vector2(SoldierRT.path[self.path_pos + 1]) \
                - Vector2(SoldierRT.path[self.path_pos])
        else:
            if self.path_pos == 0: return

            self.direction = Vector2(SoldierRT.path[self.path_pos - 1]) \
                - Vector2(SoldierRT.path[self.path_pos])

    def __update_cords(self, game_speed: float):
        '''Updates actual real position.

        Position is in float px value.
        '''
        if self.state == 'walk':
            self.cords += self.direction * TILE_SIZE * game_speed / FRAMERATE
        else:
            self.cords = Vector2(SoldierRT.path[self.path_pos]) * TILE_SIZE

    def __update_hp_rate(self):
        target = self.actual_hp / self.stats['max_hp']
        self.actual_hp_rate -= abs(target - self.actual_hp_rate) / HP_BAR_SMOOTH

    def __str__(self):
        return f'<{self.side}:{self.id} {self.cords}>'
    

        

    

    

    
        

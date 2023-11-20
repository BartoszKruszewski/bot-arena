from pygame import Vector2
from ...const import TILE_SIZE, FRAMERATE, ANIMATION_NAMES, HP_BAR_SMOOTH
from .object_rt import ObjectRT

class SoldierRT(ObjectRT):
    '''Real time soldier game_render class.
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

    def update(self, dt: float, mouse_pos: Vector2):
        super().update(dt, mouse_pos)
        self.__update_direction()
        self.__update_cords(dt)
        self.__update_animation()
        self.__update_hp_rate(dt)

    def set_state(self, state: str):
        '''Soldier state setter.

        States:
            - idle (no moving, stay in place, no animation)
            - walk (moving by the path, walking animation)
            - fight (no moving, fight animation)
        '''

        if state not in ('idle', 'walk', 'fight'):
            raise Exception('Animation not exists!')
        self.state = state

    def __update_animation(self):
        '''Updates actual animation name.
        '''
        self.animation = 'fight' if self.state == 'fight' else 'walk'

    def __update_direction(self):
        '''Updates actual direction vector.
        '''

        if self.side == 'left':
            if self['position'] != len(SoldierRT.path) - 1: 
                self.direction = Vector2(SoldierRT.path[self['position'] + 1]) \
                    - Vector2(SoldierRT.path[self['position']])
        else:
            if self['position'] != 0: 
                self.direction = Vector2(SoldierRT.path[self['position'] - 1]) \
                    - Vector2(SoldierRT.path[self['position']])

    def __update_cords(self, dt: float):
        if self.state == 'walk':
            self.cords += self.direction * TILE_SIZE * dt / FRAMERATE
        else:
            self.cords = Vector2(SoldierRT.path[self['position']]) * TILE_SIZE

    def __update_hp_rate(self, dt):
        self.actual_hp_rate = self.stats['hp'] / self.stats['max_hp']
        #self.actual_hp_rate += (self.actual_hp_rate - target) / HP_BAR_SMOOTH * dt


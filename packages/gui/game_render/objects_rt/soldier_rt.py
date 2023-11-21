from pygame import Vector2
from ...const import TILE_SIZE, FRAMERATE, HP_BAR_SMOOTH, ANIMATION_LEN
from .object_rt import ObjectRT
from ..particle import BloodParticle

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

    def update(self, dt: float, mouse_pos: Vector2, game_speed: float):
        super().update(dt, mouse_pos, game_speed)
        self.__update_direction()
        self.__update_cords(dt, game_speed)
        self.__update_animation()
        self.__update_hp_rate(dt)
        self.__update_particles()

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

    def __update_cords(self, dt: float, game_speed: float):
        if self.state == 'walk':
            self.cords += self.direction * (TILE_SIZE / FRAMERATE) * dt * game_speed
        else:
            self.cords = Vector2(SoldierRT.path[self['position']]) * TILE_SIZE

    def __update_hp_rate(self, dt):
        target = self.stats['hp'] / self.stats['max_hp']
        self.actual_hp_rate += (target - self.actual_hp_rate) / HP_BAR_SMOOTH * dt

    def __update_particles(self):
        if self.state == 'fight' and self.frame == ANIMATION_LEN - 1:
            ObjectRT.particle_controller.add_particles(
                BloodParticle,
                pos = self.cords + Vector2(TILE_SIZE) // 2,
                amount = 10,
                direction = -self.direction
            )
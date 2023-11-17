from pygame import Vector2
from ...const import FRAMERATE, TILE_SIZE, MOVE_PRECISION, PROJECTILE_SPEED
from .soldier_rt import SoldierRT
from .object_rt import ObjectRT


class ProjectileRT(ObjectRT):
    '''Real time projectile class used in game_render rendering.
    '''

    def __init__(self, cords: Vector2, id: int, side: str, target: SoldierRT):
            
        super().__init__(cords, id, 'projectile', side)
        self.target = target
        self.hit = False

    def update(self, dt: float):

        self.cords.move_towards_ip(self.target.cords, PROJECTILE_SPEED * TILE_SIZE * dt / FRAMERATE)
        if self.cords.distance_to(self.target.cords) < MOVE_PRECISION:
            self.hit = True

        if self.state != 'idle':
            super().__update_frame(dt)

    def __str__(self):
        return f'<{self.side}:{self.id} {self.cords}>'
        
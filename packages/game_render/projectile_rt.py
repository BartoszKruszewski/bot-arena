from pygame import Vector2
from .soldier_rt import SoldierRT
from .object_rt import ObjectRT
from .const import FRAMERATE, TILE_SIZE, MOVE_PRECISION, PROJECTILE_SPEED

class ProjectileRT(ObjectRT):
    '''Real time projectile class used in game_render rendering.
    '''

    def __init__(self, cords: Vector2, id: int, side: str, target: SoldierRT):
            
        # data
        self.cords = cords
        self.id = id
        self.side = side
        self.target = target
        self.hit = False

        # state
        self.frame = 0
        self.tick = 0
        self.state = 'idle'

    def update(self, game_speed: float):

        self.cords.move_towards_ip(self.target.cords, PROJECTILE_SPEED * TILE_SIZE * game_speed / FRAMERATE)
        if self.cords.distance_to(self.target.cords) < MOVE_PRECISION:
            self.hit = True

        if self.state != 'idle':
            super().__update_frame(game_speed)

    def __str__(self):
        return f'<{self.side}:{self.id} {self.cords}>'
        
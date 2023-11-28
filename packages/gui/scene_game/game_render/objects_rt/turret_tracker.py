from pygame import Vector2

from .object_rt import ObjectRT
from .....game_logic.objects.turrets import Turret
from .turret_rt import TurretRT
from .object_tracker import ObjectTracker

class TurretTracker(ObjectTracker):
    def get_new_object(self, logic_object, side: str) -> ObjectRT:
        return TurretRT(
            Vector2(logic_object.cords),
            logic_object.id,
            'turret',
            side,
            logic_object.__dict__()
        )
    
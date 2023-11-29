from pygame import Vector2

from packages.game_logic.objects.farms import Farm
from .object_rt import ObjectRT
from .farm_rt import FarmRT
from .object_tracker import ObjectTracker

class FarmTracker(ObjectTracker):
    def get_new_object(self, logic_object: Farm, side: str) -> ObjectRT:
        return FarmRT(
            Vector2(logic_object.cords),
            logic_object.id,
            'farm',
            side,
            logic_object.__dict__()
        )

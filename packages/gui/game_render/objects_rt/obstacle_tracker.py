from pygame import Vector2

from ....game_logic.objects.obstalces import Obstacle
from .object_rt import ObjectRT
from .obstacle_rt import ObstacleRT
from .object_tracker import ObjectTracker
from random import randint
from ...const import OBSTACLE_TYPE_NUMBER

class ObstacleTracker(ObjectTracker):
    def get_new_object(self, logic_object: Obstacle, side: str) -> ObjectRT:
        return ObstacleRT(
            Vector2(logic_object.cords),
            logic_object.id,
            str(randint(1, OBSTACLE_TYPE_NUMBER)),
            side,
            logic_object.__dict__()
        )

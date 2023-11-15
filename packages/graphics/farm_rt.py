from pygame import Vector2
from.object_rt import ObjectRT

class FarmRT(ObjectRT):
    def __init__(self, cords: Vector2, id: int, name: str, side: str, stats: dict):
        super().__init__(cords, id, name, side, stats)

    def update(self, game_speed: float, mouse_pos: Vector2):
        super().update(game_speed, mouse_pos)
    
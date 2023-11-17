from pygame import Vector2
from .object_rt import ObjectRT

class TurretRT(ObjectRT):
    '''Real time turret class used in game_render rendering.
    '''

    def __init__(self, cords: Vector2, id: int, name: str, side: str, stats: dict) -> None:
        super().__init__(cords, id, name, side, stats)

    def update(self, dt: float, mouse_pos: Vector2): 
        super().update(dt, mouse_pos)
from .object_rt import ObjectRT
from pygame import Vector2

class TurretRT(ObjectRT):
    '''Real time turret class used in graphics rendering.
    '''

    def __init__(self, cords: Vector2, id: int, name: str, side: str) -> None:
        super().__init__(cords, id, name, side)

    def update(self, game_speed: float, mouse_pos: Vector2): 
        super().update(game_speed, mouse_pos)
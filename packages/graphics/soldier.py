from pygame import Vector2
from .const import FRAMERATE, ANIMATION_SPEED, ANIMATION_LEN, TILE_SIZE
from ..game_logic.stats import ROUND_LEN

class Soldier():
    def __init__(self) -> None:
        self.pos = Vector2(0, 0)
        self.real_pos = Vector2(0, 0)
        self.next_pos = Vector2(0, 0)

    def __update_real_pos(self):
        self.real_pos += (self.next_pos - self.pos) * TILE_SIZE * ROUND_LEN / FRAMERATE / 1000
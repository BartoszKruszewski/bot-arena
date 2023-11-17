from pygame import Vector2
from .farm_rt import FarmRT
from ..game_logic.objects.farms import Farm

class FarmTracker():
    '''Farm objects tracker.

    Track Farm objects from game logic and
    synchronize them with real time FarmRT
    objects in the game_render module.
    '''

    def __init__(self):
        self.farms_rt = {"left": {}, "right": {}}

    def update_tracker(self, farms: dict[str, list[Farm]]):
        self.spawn_new_farms(farms["left"], "left")
        self.spawn_new_farms(farms["right"], "right")

    def spawn_new_farms(self, side_farms: list[Farm], side: str):
        for farm in side_farms:
            if farm.id not in self.farms_rt[side]:
                self.farms_rt[side][farm.id] = FarmRT(
                    Vector2(farm.cords),
                    farm.id,
                    'farm',
                    side,
                    farm.__dict__()
                )

    def update_farms(self, game_speed: float, mouse_pos: Vector2) -> None:
        '''Updates every real time farm.
        '''

        for farm in self.get_farms():
            farm.update(game_speed, mouse_pos)
    
    def get_farms(self) -> list[FarmRT]:
        '''Real time farms getter.
        '''

        return list(self.farms_rt['left'].values()) + \
              list(self.farms_rt['right'].values())
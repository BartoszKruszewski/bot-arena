from pygame import Vector2
from .turret_rt import TurretRT
from ..game_logic.objects.turrets import Turret

class TurretTracker():
    '''Turret objects tracker.

    Track Turret objects from game logic and
    synchronize them with real time TurretRT
    objects in the graphics module. 
    '''

    def __init__(self):
        self.turrets_rt = {"left": {}, "right": {}}

    def update_tracker(self, turrets: dict[str, list[Turret]]):
        self.spawn_new_turrets(turrets["left"], "left")
        self.spawn_new_turrets(turrets["right"], "right")

    def spawn_new_turrets(self, side_turrets: list[Turret], side: str):
        for turret in side_turrets:
            if turret not in self.turrets_rt:
                self.turrets_rt[side][turret.id] = TurretRT(
                    Vector2(turret.cords),
                    turret.id
                )

    def update_turrets(self, game_speed: float) -> None:
        '''Updates every real time turret.
        '''

        for turret in self.get_turrets():
            turret.update(game_speed)
    
    def get_turrets(self) -> list[TurretRT]:
        '''Real time turrets getter.
        '''

        return list(self.turrets_rt['left'].values()) + \
              list(self.turrets_rt['right'].values())
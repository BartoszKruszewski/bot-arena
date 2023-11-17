from pygame import Vector2
from ....game_logic.objects.turrets import Turret
from ....game_logic.objects.soldiers import Soldier
from ...const import TILE_SIZE
from .soldier_tracker import SoldierTracker
from .projectile_rt import ProjectileRT


class ProjectileTracker:

    def __init__(self, path: list[tuple]):
        self.projectiles_rt = {"left": {}, "right": {}}
        self.next_id = 0
        self.path = path

    def update_tracker(self, soldiers: list[Soldier], soldier_tracker:SoldierTracker, turrets: list[Turret], is_new_turn):
        def spawn_new_projectiles(soldiers: list[Soldier], soldier_tracker: SoldierTracker, turrets: list[Turret], turret_side: str, soldier_side: str):
            for turret in turrets[turret_side]:
                for soldier in soldiers[soldier_side]:
                    # print('\n\n', soldier, '\)
                    if soldier.position < 0 or soldier.position >= len(self.path): break
                    if turret._is_in_range(self.path[soldier.position]):
                        self.projectiles_rt[turret_side][self.next_id] = ProjectileRT(
                            Vector2(turret.cords) * TILE_SIZE,
                            self.next_id,
                            turret_side,
                            soldier_tracker.soldiers_rt[soldier_side][soldier.id]
                        )
                        self.next_id += 1
                        break
        if is_new_turn:
            spawn_new_projectiles(soldiers, soldier_tracker, turrets, "left", "right")
            spawn_new_projectiles(soldiers, soldier_tracker, turrets, "right", "left")

        def remove_projectiles(side: str):
            projectiles_to_remove = []
            for id in self.projectiles_rt[side]:
                if self.projectiles_rt[side][id].hit:
                    projectiles_to_remove.append(id)
            for id in projectiles_to_remove:
                self.projectiles_rt[side].pop(id)
        
        remove_projectiles("left")
        remove_projectiles("right")

    def update_projectiles(self, dt: float):
        for projectile in self.get_projectiles():
            projectile.update(dt)

    def get_projectiles(self) -> list[ProjectileRT]:
        '''Real time projectiles getter.
        '''

        return list(self.projectiles_rt['left'].values()) + \
              list(self.projectiles_rt['right'].values())
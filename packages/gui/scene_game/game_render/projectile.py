from math import degrees, atan2
from pygame import Vector2
from .objects_rt.soldier_rt import SoldierRT
from .objects_rt.turret_rt import TurretRT
from .particle import ParticleController, BloodParticle
from ...const import FRAMERATE, MOVE_PRECISION, PROJECTILE_SPEED

class Projectile:
    def __init__(self, pos: Vector2, target: SoldierRT):
        self.pos = pos.copy()
        self.hit = False
        self.angle = 0
        self.__target = target
        self.__all_distance = self.pos.distance_to(self.__target.cords)
    
    def update(self, dt: float, game_speed: float):
        self.pos.move_towards_ip(
            self.__target.cords,
            self.__all_distance / FRAMERATE * game_speed * dt * PROJECTILE_SPEED
        )
        self.angle = degrees(atan2(
            -(self.__target.cords.y - self.pos.y),
            self.__target.cords.x - self.pos.x)) + degrees(90)

        if self.pos.distance_to(self.__target.cords) <= MOVE_PRECISION:
            self.hit = True

class ProjectileController:
    def __init__(self, path) -> None:
        self.__projectiles = []
        self.__tick = 0
        self.__path = path

    def __distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def update_projectiles(self, turrets: list[TurretRT], soldiers: list[SoldierRT], dt: float, game_speed: float):
        self.__tick += dt * game_speed

        if self.__tick >= FRAMERATE:
            self.__tick %= FRAMERATE
            
            # Check for possible shots from turrets.
            for side in ("left", "right"):
                for turret in filter(lambda t: t.side == side, turrets):
                    for soldier in filter(lambda s: s.side != side, soldiers):
                        pos = self.__path[soldier['position'] + (1 if side == 'right' else -1)]
                        if self.__distance(turret['cords'], pos) <= turret.stats["range"]:
                            self.__projectiles.append(Projectile(turret.cords, soldier))
                            break

            # Check for possible shots from soldiers.
            for side in ("left", "right"):
                for soldier in filter(lambda s: s.side == side, soldiers):
                    if not soldier.stats["range"] > 1: continue 
                    for enemy in filter(lambda s: s.side != side, soldiers):
                        pos1 = self.__path[soldier['position']]
                        pos2 = self.__path[enemy['position']]
                        if self.__distance(pos1, pos2) <= soldier.stats["range"]:
                            self.__projectiles.append(Projectile(soldier.cords, enemy))
                            break
        
        # Remove projectiles that hit the target.
        self.__projectiles = [p for p in self.__projectiles if not p.hit]

        # Update projectiles' states.
        for projectile in self.__projectiles:
            projectile.update(dt, game_speed)

    def get_projectiles(self):
        return self.__projectiles
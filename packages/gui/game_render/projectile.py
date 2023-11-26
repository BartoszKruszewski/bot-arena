from math import degrees, atan2
from pygame import Vector2
from .objects_rt.soldier_rt import SoldierRT
from .objects_rt.turret_rt import TurretRT
from .particle import ParticleController, BloodParticle
from ..const import FRAMERATE, MOVE_PRECISION, TILE_SIZE

class Projectile:

    def __init__(self, pos: Vector2, id: int, target: SoldierRT):
        self.pos = pos.copy()
        self.hit = False
        self.angle = 0
        self.__target = target
        self.__distance = ((self.pos.x - self.__target.cords.x)**2 + (self.pos.y - self.__target.cords.y)**2)**(1/2)
        self.__id = id
    
    def update(self, dt: float, game_speed: float):
        self.pos.move_towards_ip(self.__target.cords, self.__distance / FRAMERATE * game_speed * dt)
        self.angle = degrees(atan2(-(self.__target.cords.y - self.pos.y), self.__target.cords.x - self.pos.x)) + degrees(90)
        distance = ((self.pos.x - self.__target.cords.x)**2 + (self.pos.y - self.__target.cords.y)**2)**(1/2)

        if distance <= MOVE_PRECISION:
            self.hit = True

class ProjectileController:
    def __init__(self) -> None:
        self.__projectiles = []
        self.__next_id = 0
        self.__tick = 0

    def update_projectiles(self, turrets: list[TurretRT], soldiers: list[SoldierRT], dt: float, game_speed: float):
        sides = ("left", "right")
        self.__tick += dt

        def getDistance(pos1, pos2):
            return ((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)**(1/2)

        if self.__tick >= FRAMERATE / game_speed:
            self.__tick %= (FRAMERATE / game_speed)
            
            # Check for possible shots from turrets.
            for side in sides:
                for turret in filter(lambda t: t.side == side, turrets):
                    for soldier in filter(lambda s: s.side != side, soldiers):
                        distance = getDistance(turret.cords, soldier.cords)
                        if distance < turret.stats["range"] * TILE_SIZE:
                            self.__projectiles.append(Projectile(turret.cords, self.__next_id, soldier))
                            self.__next_id += 1
                            break

            # Check for possible shots from soldiers.
            for side in sides:
                for shooter in filter(lambda s: s.side == side, soldiers):
                    for shot in filter(lambda s: s.side != side, soldiers):
                        if not shooter.stats["range"] > 1: continue 
                        if shooter.stats["range"] * TILE_SIZE >= getDistance(shooter.cords, shot.cords):
                            self.__projectiles.append(Projectile(shooter.cords, self.__next_id, shot))
                            self.__next_id += 1
                            break
        
        # Remove projectiles that hit the target.
        self.__projectiles = [i for i in filter(lambda p: p.hit == False, self.__projectiles)]

        # Update projectiles' states.
        for projectile in self.__projectiles:
            projectile.update(dt, game_speed)

    def get_projectiles(self):
        return self.__projectiles
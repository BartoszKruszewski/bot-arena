from pygame import Vector2, Color
from random import randint
from .const import PARTICLE_DIRECTION_PRECISION as PDP, STANDARD_PARTICLE_TIME, \
    STANDARD_PARTICLE_SPEED, FRAMERATE, STANDARD_PARTICLE_ACC

class Particle:
    def __init__(self,
            pos: Vector2,
            color: Color,
            size: int = 1,
            speed: float = STANDARD_PARTICLE_SPEED,
            fading: bool = True,
            time: float = STANDARD_PARTICLE_TIME,
            acc: float = STANDARD_PARTICLE_ACC
        ):

        self.__pos = pos.copy()
        self.__color = color
        self.__size = randint(1, size)
        self.__fading = fading
        self.__movement = Vector2(
            randint(-PDP, PDP) / PDP, 
            randint(-PDP, PDP) / PDP, 
        ) * speed
        self.__tick = 0
        self.__time = randint(1, time)
        self.__max_time = time

    def is_alive(self) -> bool:
        return self.__time > 0

    def get_data(self) -> tuple[Vector2, Color, int]:
        '''Return particle data.

        tuple[position, color, size]
        '''

        return self.__pos, self.__color, self.__size

    def update(self, game_speed: float):
        self.__tick += 1
        if self.__tick > FRAMERATE / game_speed / 10:
            self.__time -= 1
            self.__tick = 0
        self.__movement *= STANDARD_PARTICLE_ACC
        self.__pos += self.__movement / game_speed
        if self.__fading:
            self.__color.a = min(max(int(255  * self.__time / self.__max_time), 0), 255)

    def __str__(self) -> str:
        return f'<{self.__class__}: {self.__pos}>'

class BloodParticle(Particle):
    def __init__(self, pos: Vector2):
        super().__init__(pos, Color(255, 0, 0))

class ParticleController:
    def __init__(self):
        self.__particles = []

    def update_particles(self, game_speed: float):
        for particle in self.__particles:
            particle.update(game_speed)
        self.__particles = [particle for particle in self.__particles if particle.is_alive()]

    def get_particles(self) -> list[Particle]:
        return self.__particles
    
    def add_particles(self, particle_type: type, pos: Vector2, amount: int):
        for _ in range(amount):
            self.__particles.append(particle_type(pos))
            

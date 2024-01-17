from pygame import Vector2, Color
from pygame.font import Font
from random import randint
from packages.gui.const import PARTICLE_DIRECTION_PRECISION as PDP, STANDARD_PARTICLE_TIME, \
    STANDARD_PARTICLE_SPEED, FRAMERATE, STANDARD_PARTICLE_ACC, STANDARD_PARTICLE_SIZE


class Particle:
    def __init__(self, pos: Vector2, color: Color, **kwargs):

        speed = STANDARD_PARTICLE_SPEED if not 'speed' in kwargs else kwargs['speed']
        size = STANDARD_PARTICLE_SIZE if not 'size' in kwargs else kwargs['size']
        time = STANDARD_PARTICLE_TIME if not 'time' in kwargs else kwargs['time']
        acc = STANDARD_PARTICLE_ACC if not 'acc' in kwargs else kwargs['acc']
        direction = Vector2(
            randint(-PDP, PDP) / PDP, 
            randint(-PDP, PDP) / PDP, 
        ) if not 'direction' in kwargs else kwargs['direction']
        fading = True if not 'fading' in kwargs else kwargs['fading']
        texture = None if not 'texture' in kwargs else kwargs['texture']

        self.__texture = texture
        self.__pos = pos.copy()
        self.__color = color
        self.__max_opacity = color.a
        self.__size = randint(1, size)
        self.__fading = fading
        self.__direction = (direction + Vector2(randint(-PDP, PDP) / PDP, randint(-PDP, PDP) / PDP)).normalize()
        self.__speed = randint(int(0.8 * PDP), PDP) / PDP * speed
        self.__time = randint(1, time)
        self.__max_time = time
        self.__acc = randint(int(0.8 * PDP), PDP) / PDP * acc

    def is_alive(self) -> bool:
        '''Returns True when particle should be displayed.
        '''

        return self.__time > 0

    def get_data(self) -> tuple[Vector2, Color, int]:
        '''Return particle data.

        tuple[position, color, size]
        '''
        return self.__pos, self.__color, self.__size, self.__texture

    def update(self, dt: float, game_speed: float):
        '''Main update function.

        Refreshes once per frame.
        '''

        self.__time -= dt * game_speed
        self.__speed *= self.__acc * dt
        self.__pos += self.__direction * self.__speed * dt
        if self.__fading:
            self.__color.a = min(max(int(self.__max_opacity  * self.__time / self.__max_time), 0), 255)

    def __str__(self) -> str:
        return f'<{self.__class__}: {self.__pos}>'

class DamageInfoParticle(Particle):
    def __init__(self, pos: Vector2, **kwargs):
        super().__init__(
            pos, Color(255, 0, 0, 200),
            direction = kwargs['direction'],
            speed = 6,
            time = 100,
            acc = 0.9,
            texture = Font(f'./assets/font.ttf', 8).render(str(kwargs['value']), False, kwargs['text_color'])

        )

class BloodParticle(Particle):
    def __init__(self, pos: Vector2, **kwargs):
        super().__init__(
            pos, Color(255, 0, 0, 200),
            direction = kwargs['direction'],
            size = 4,
            speed = 9,
            time = 100,
            acc = 0.8
        )

class ParticleController:
    '''Main class controlling particles. 
    '''

    def __init__(self):
        self.__particles = []

    def update_particles(self, dt: float, game_speed: float) -> None:
        '''Updates all particles.
        '''

        for particle in self.__particles:
            particle.update(dt, game_speed)
        self.__particles = [particle for particle in self.__particles if particle.is_alive()]

    def get_particles(self) -> list[Particle]:
        '''Gets all particles list.
        '''

        return self.__particles
    
    def add_particles(self, particle_type: type, pos: Vector2, **kwargs) -> None:
        '''Add particles in declared position.
        '''

        for _ in range(kwargs['amount'] if 'amount' in kwargs else 1):
            self.__particles.append(particle_type(pos, **kwargs))
            

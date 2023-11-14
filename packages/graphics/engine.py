from pygame import Surface, SRCALPHA
from pygame import Vector2

from .const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, \
    TILE_SIZE, SHOW_SOLDIERS_REAL_POS, SHOW_FARMS_REAL_POS, \
    SPRITE_SIZE, SHOW_TURRETS_REAL_POS
from .camera import Camera
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer
from ..game_logic.game import Game
from .soldier_rt import SoldierRT
from .soldier_tracker import SoldierTracker
from .turret_rt import TurretRT
from .turret_tracker import TurretTracker
from .farm_rt import FarmRT
from .farm_tracker import FarmTracker
from .particle import ParticleController, Particle, BloodParticle

class Engine():
    '''Main graphics class.
    '''

    def __init__(self, game: Game):

        # render surface
        self.__draw_screen = Surface(DRAW_SCREEN_SIZE)
        
        # initialize modules
        self.__map_renderer = MapRenderer(game)
        self.__soldier_tracker = SoldierTracker(game.get_path())
        self.__turret_tracker = TurretTracker()
        self.__farm_tracker = FarmTracker()
        self.__particle_controller = ParticleController()
        self.__camera = Camera(game.get_map_size())

        # assets
        self.__assets_loader = AssetsLoader()
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + '/' + 'textures'
        self.__assets = self.__assets_loader.load(path, '.png')

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game)

    def render(self, game: Game, game_speed: float) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''

        # update staff
        self.__camera.update()
        self.__soldier_tracker.update_tracker(game.get_soldiers(), self.__particle_controller)
        self.__soldier_tracker.update_soldiers(game_speed)
        self.__turret_tracker.update_tracker(game.get_turrets())
        self.__turret_tracker.update_turrets(game_speed)
        self.__farm_tracker.update_tracker(game.get_farms())
        self.__farm_tracker.update_farms(game_speed)
        self.__particle_controller.update_particles(game_speed)

        # reset frame
        self.__draw_screen.fill((0, 0, 0))

        # drawing soldiers and their health bars
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())
        for soldier in self.__soldier_tracker.get_soldiers():
            self.__draw_soldier(soldier)

        # drawing turrets
        for turret in self.__turret_tracker.get_turrets():
            self.__draw_turret(turret)

        # drawing farms
        for farm in self.__farm_tracker.get_farms():
            self.__draw_farm(farm)

        # drawing particles
        for particle in self.__particle_controller.get_particles():
            self.__draw_particle(particle)

        return self.__draw_screen

    def __draw_soldier(self, soldier: SoldierRT) -> None:
        '''Draw soldier object on the screen.
        '''
        direction = {
            (0, 0):    'bot',
            (0, -1):   'top',
            (0, 1):    'bot',
            (-1, 0):   'left',
            (1, 0):    'right'
        }[(int(soldier.direction.x), int(soldier.direction.y))]

        texture = self.__assets['soldiers'][soldier.name] \
            [soldier.animation][direction][soldier.frame]

        self.__draw(
            texture,
            soldier.real_pos + \
            Vector2(TILE_SIZE // 2, TILE_SIZE // 2) \
            - Vector2(texture.get_size()) // 2
        )

        size = texture.get_size()[0] -4
        bar = Surface((size, 1))
        bar.fill((255, 0, 0))
        self.__draw(bar, soldier.real_pos - Vector2(-1, 4))

        bar = Surface((soldier.actual_hp_rate * size, 1))
        bar.fill((0, 255, 0))
        self.__draw(bar, soldier.real_pos - Vector2(-1, 4))

        # real pos
        if SHOW_SOLDIERS_REAL_POS:
            surf = Surface((1, 1))
            surf.fill((255, 0, 0))
            self.__draw(surf, soldier.real_pos)

    def __draw_turret(self, turret: TurretRT) -> None:
        '''Draw turret object on the screen.
        '''

        texture = self.__assets["turrets"]["turret"]

        size = texture.get_size()

        self.__draw(
            texture,
            turret.cords + \
            Vector2(TILE_SIZE // 2, TILE_SIZE - size[1]) \
            - Vector2(size[0], 0) // 2
        )
        
        # real pos
        if SHOW_TURRETS_REAL_POS:
            surf = Surface((TILE_SIZE, TILE_SIZE))
            surf.set_alpha(70)
            surf.fill((255, 0, 0))
            self.__draw(surf, Vector2(turret.cords))

    def __draw_farm(self, farm: FarmRT) -> None:
        '''Draw farm object on the screen.
        '''

        texture = self.__assets["farms"]["farm"]

        size = texture.get_size()

        self.__draw(
            texture,
            farm.cords + \
            Vector2(TILE_SIZE // 2, TILE_SIZE - size[1]) \
            - Vector2(size[0], 0) // 2
        )
        
        # real pos
        if SHOW_FARMS_REAL_POS:
            surf = Surface((TILE_SIZE, TILE_SIZE))
            surf.set_alpha(70)
            surf.fill((255, 0, 0))
            self.__draw(surf, Vector2(farm.cords))

    def __draw_particle(self, particle: Particle):
        pos, color, size = particle.get_data()
        surf = Surface((size, size), SRCALPHA)
        surf.fill(color)
        self.__draw(surf, pos)

    def __draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.__camera.get_offset().x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.__camera.get_offset().y <= DRAW_SCREEN_SIZE_Y:
            self.__draw_screen.blit(texture, pos + self.__camera.get_offset())
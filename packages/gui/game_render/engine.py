from pygame import Surface, SRCALPHA, Rect, Color
from pygame import Vector2
from pygame.draw import rect as draw_rect, line as draw_line
from pygame.transform import scale
from ...game_logic.game import Game
from math import floor

from ..const import TILE_SIZE, SHOW_REAL_POS, INFO_TAB_MARGIN, HEALTH_BAR_SIZE, \
    HEALTH_BAR_COLOR_BACK, HEALTH_BAR_COLOR_FRONT, INFO_TAB_SHOW_TIME, INFO_TAB_SHOW_SMOOTH
from ..mouse import Mouse

from .camera import Camera
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer
from .particle import ParticleController, Particle
from .font_renderer import FontRenderer

from .objects_rt.soldier_rt import SoldierRT
from .objects_rt.object_rt import ObjectRT
from .objects_rt.soldier_tracker import SoldierTracker
from .objects_rt.turret_rt import TurretRT
from .objects_rt.turret_tracker import TurretTracker
from .objects_rt.farm_rt import FarmRT
from .objects_rt.farm_tracker import FarmTracker
from .objects_rt.obstacle_tracker import ObstacleTracker
from .objects_rt.obstacle_rt import ObstacleRT
from .draw import Draw

class Engine():
    '''Main game_render class.
    '''

    def __init__(self, game: Game):

        # initialize modules
        self.__particle_controller = ParticleController()
        self.__assets_loader = AssetsLoader()
        self.__camera = Camera(game.get_map_size())

        self.__draw = Draw(
            self.__assets_loader.load('./assets/textures', '.png'), game)

        self.__soldier_tracker = SoldierTracker(game.get_path(), self.__particle_controller)
        self.__turret_tracker = TurretTracker(self.__particle_controller)
        self.__farm_tracker = FarmTracker(self.__particle_controller)
        self.__obstacle_tracker = ObstacleTracker(self.__particle_controller)
        
    def render(
            self, game: Game, dt: float, draw_screen_size: Vector2,
            mouse: Mouse, screen_shift: Vector2, zoom: float, game_speed: float
        ) -> Surface:

        '''Main rendering function.

        Refereshes once per frame.
        '''

        # update staff
        self.__camera.update(draw_screen_size, mouse, screen_shift, zoom, dt)
        self.__soldier_tracker.update(
            game.get_soldiers(), dt, self.__camera.get_mouse_pos(), game_speed)
        self.__turret_tracker.update(
            game.get_turrets(), dt, self.__camera.get_mouse_pos(), game_speed)
        self.__farm_tracker.update(
            game.get_farms(), dt, self.__camera.get_mouse_pos(), game_speed)
        self.__obstacle_tracker.update(
            {'left': game.get_obstacles(), 'right': []},
            dt, self.__camera.get_mouse_pos(), game_speed
        )
        self.__particle_controller.update_particles(dt)

        # reset frame
        self.__draw.begin(self.__camera.get_offset(), draw_screen_size)
        
        # draw objects
        objects_queue = []

        for tracker in self.__soldier_tracker, self.__farm_tracker, \
         self.__turret_tracker, self.__obstacle_tracker:
            for object in tracker.get_objects():
                objects_queue.append(object)

        for object in sorted(objects_queue, key = lambda x: x.cords.y):
            self.__draw.object_rt(object)

        # draw particles
        for particle in self.__particle_controller.get_particles():
            self.__draw.particle(particle)

        return scale(
            self.__draw.end(),
            Vector2(
                draw_screen_size) * zoom
        )

    
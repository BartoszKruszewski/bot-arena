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

class Engine():
    '''Main game_render class.
    '''

    def __init__(self, game: Game):

        # initialize modules
        self.__map_renderer = MapRenderer()
        self.__particle_controller = ParticleController()
        self.__font_renderer = FontRenderer()
        self.__assets_loader = AssetsLoader()
        self.__camera = Camera(game.get_map_size())

        self.__soldier_tracker = SoldierTracker(game.get_path())
        self.__turret_tracker = TurretTracker()
        self.__farm_tracker = FarmTracker()
        self.__obstacle_tracker = ObstacleTracker()

        # assets
        self.__assets = self.__assets_loader.load('./assets/textures', '.png')

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game)
        
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
        self.__draw_screen = Surface(draw_screen_size // zoom)
        self.__ui_texture = Surface(draw_screen_size // zoom, SRCALPHA)
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())
        
        # draw objects
        objects_queue = []

        for tracker in self.__soldier_tracker, self.__farm_tracker, \
         self.__turret_tracker, self.__obstacle_tracker:
            for object in tracker.get_objects():
                objects_queue.append(object)

        for object in sorted(objects_queue, key = lambda x: x.cords.y):
            self.__draw_object_rt(object)

        # draw particles
        for particle in self.__particle_controller.get_particles():
            self.__draw_particle(particle)
        
        # draw ui
        self.__draw_screen.blit(self.__ui_texture, (0, 0))

        return scale(
            self.__draw_screen,
            Vector2(self.__draw_screen.get_size()) * zoom
        )

    def __draw_projectile(self, projectile):
            texture = self.__assets["projectiles"]["arrow"]
            size = texture.get_size()
            self.__draw(
                texture,
                projectile.cords + \
                Vector2(TILE_SIZE // 2, TILE_SIZE - size[1]) \
                - Vector2(size[0], 0) // 2
            )

    def __draw_object_rt(self, object: ObjectRT):
        
        if object.__class__ == SoldierRT:
            direction = {
                (0, 0):    'bot',
                (0, -1):   'top',
                (0, 1):    'bot',
                (-1, 0):   'left',
                (1, 0):    'right'
            }[tuple(object.direction)]

            texture = self.__assets['soldiers'][object.name] \
            [object.animation][direction][object.frame]

            self.__draw_health_bar(object)

        elif object.__class__ == FarmRT:
            texture = self.__assets["farms"]["farm"]
        elif object.__class__ == TurretRT:
            texture = self.__assets["turrets"]["turret"]
        elif object.__class__ == ObstacleRT:
            texture = self.__assets["obstacles"]["obstacle_" + object.name]
        else:
            raise Exception(f'{object} is not a real time object!')        

        size = texture.get_size()

        self.__draw(texture,
             object.cords + Vector2((TILE_SIZE - size[0]) // 2, TILE_SIZE - size[1]))
            
        self.__draw_info_bar(object.stats, object.cords, object.select_time / INFO_TAB_SHOW_TIME)

        # real pos
        if SHOW_REAL_POS:
            surf = Surface((1, 1))
            surf.fill((255, 0, 0))
            self.__draw(surf, object.cords)

    def __draw_health_bar(self, soldier: SoldierRT):
        '''Draws health bar above the soldier
        '''

        bar = Surface(HEALTH_BAR_SIZE)
        bar.fill(HEALTH_BAR_COLOR_BACK)
        bar.fill(
            HEALTH_BAR_COLOR_FRONT,
            Rect(0, 0,
                soldier.actual_hp_rate * HEALTH_BAR_SIZE[0],
                HEALTH_BAR_SIZE[1]
            )
        )
        self.__draw(
            bar,
            soldier.cords + Vector2(TILE_SIZE - HEALTH_BAR_SIZE[0], -1) // 2
        )
    
    def __draw_info_bar(self, info: dict[str, str], pos: Vector2, animation_progress: float):
        '''Draws info bar with animation.
        
        info: {
            'stat_name' : value
            ...
        }

        pos: start point cords
        animation_progress: 0 -> 1 
        '''

        def f(x, b):
            A = INFO_TAB_SHOW_SMOOTH
            return (x / (b * 1.01) - floor(x / (b * 1.01))) ** (1 / A)

        if animation_progress > 0:
            
            animation_len = 5 + len(info)
            p = 1 / animation_len
            view_rate = [
                f(max(0, animation_progress - i * p), p)
                if animation_progress < (i + 1) * p else 1
                for i in range(animation_len)
            ]

            text_surfaces = [
                self.__font_renderer.render(f'{name}: {info}', 'small')
                for name, info in info.items()
            ]

            size = Vector2(
                max(s.get_size()[0] for s in text_surfaces) + INFO_TAB_MARGIN * 2,
                sum((s.get_size()[1] for s in text_surfaces)) + INFO_TAB_MARGIN * 2,
            )

            info_tab = Surface(size, SRCALPHA)
            info_tab.fill((0, 0, 0, 120))

            for i, s in enumerate(text_surfaces):
                info_tab.blit(s.subsurface(
                    Rect(0, 0, view_rate[4 + i] * s.get_size()[0], s.get_size()[1])),
                    (INFO_TAB_MARGIN, INFO_TAB_MARGIN + \
                     sum(s.get_size()[1] for s in text_surfaces[:i])
                ))

            draw_rect(info_tab, (0, 0, 0, 0), Rect(
                0, size.y * view_rate[4] + 1, 
                size.x,
                size.y
            ))

            direction = pos.x - size.x + self.__camera.get_offset().x > 0

            draw_points = (
                Vector2(0, -1),
                Vector2(-size.x - 1, -1),
                Vector2(-size.x - 1, size.y),
                Vector2(0, size.y),
                Vector2(0, 0),
            ) if direction else (
                Vector2(0, -1),
                Vector2(size.x, -1),
                Vector2(size.x, size.y),
                Vector2(-1, size.y),
                Vector2(-1, -1),
            )
            
            frame_offset = Vector2(0, 0) if direction else Vector2(TILE_SIZE, 0)

            for i in range(1, len(draw_points)):
                if view_rate[i - 1] > 0:
                    self.__draw_line(
                        pos + frame_offset + draw_points[i - 1],
                        pos + frame_offset + draw_points[i],
                        Color(255, 255, 255),
                        view_rate[i - 1],
                        True
                    )
            
            tab_offset = Vector2(-size.x, 0) if direction else Vector2(TILE_SIZE, 0)

            if view_rate[4] > 0:
                self.__draw(
                    info_tab,
                    pos + tab_offset ,
                    True
                )

    def __draw_particle(self, particle: Particle):
        '''Draws particle.
        '''

        pos, color, size = particle.get_data()
        surf = Surface((size, size), SRCALPHA)
        surf.fill(color)
        self.__draw(surf, pos)
    
    def __draw_line(self, pos1: Vector2, pos2: Vector2, color: Color,
            len: float = 1, ui: bool = False):
        '''Draw line with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        pos2_real = pos1.move_towards(pos2, pos1.distance_to(pos2) * len)

        size = Vector2(
            abs(pos1.x - pos2_real.x),
            abs(pos1.y - pos2_real.y),
        )
        
        ca = self.__camera.get_offset()
        dss = self.__draw_screen.get_size()

        if all((
            -size.x <= pos1.x + ca.x <= dss[0],
            -size.y <= pos1.y + ca.y <= dss[1], 
            -size.x <= pos2_real.x + ca.x <= dss[0],
            -size.y <= pos2_real.y + ca.y <= dss[1],
        )):
            draw_line(
                self.__ui_texture if ui else self.__draw_screen,
                color, pos1 + ca, pos2_real + ca
            )

    def __draw(self, texture: Surface, pos: Vector2, ui: bool = False) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        ca = self.__camera.get_offset()
        dss = self.__draw_screen.get_size()

        size = Vector2(texture.get_size())
        if all((
            -size.x <= pos.x + ca.x <= dss[0],
            -size.y <= pos.y + ca.y <= dss[1],
        )):
            if ui: self.__ui_texture.blit(texture, pos + ca)
            else: self.__draw_screen.blit(texture, pos + ca)
from pygame import Surface, SRCALPHA, Rect, Color
from pygame import Vector2
from pygame.draw import rect as draw_rect, line as draw_line
from pygame.transform import scale
from ...game_logic.game import Game

from ..const import TILE_SIZE, SHOW_REAL_POS, INFO_TAB_MARGIN
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
from .objects_rt.projectile_tracker import ProjectileTracker

class Engine():
    '''Main game_render class.
    '''

    def __init__(self, game: Game):

        # initialize modules
        self.__map_renderer = MapRenderer(game)
        self.__soldier_tracker = SoldierTracker(game.get_path())
        self.__turret_tracker = TurretTracker()
        self.__farm_tracker = FarmTracker()
        self.__projectile_tracker = ProjectileTracker(game.get_path())
        self.__particle_controller = ParticleController()
        self.__font_renderer = FontRenderer()
        self.__camera = Camera(game.get_map_size())
        self.__draw_screen = None
        self.__ui_texture = None

        # assets
        self.__assets_loader = AssetsLoader()
        self.__assets = self.__assets_loader.load('./assets/textures', '.png')

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game)
        
    def render(self, game: Game, dt: float, is_new_turn: bool, draw_screen_size: Vector2, mouse: Mouse, screen_shift: Vector2, zoom: float) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''

        # update staff
        self.__camera.update(draw_screen_size, mouse, screen_shift, zoom)
        self.__soldier_tracker.update_tracker(game.get_soldiers(), self.__particle_controller)
        self.__soldier_tracker.update_soldiers(dt, self.__camera.get_mouse_pos())
        self.__turret_tracker.update_tracker(game.get_turrets())
        self.__turret_tracker.update_turrets(dt, self.__camera.get_mouse_pos())
        self.__farm_tracker.update_tracker(game.get_farms())
        self.__farm_tracker.update_farms(dt, self.__camera.get_mouse_pos())
        self.__projectile_tracker.update_tracker(game.get_soldiers(), self.__soldier_tracker, game.get_turrets(), is_new_turn)
        self.__projectile_tracker.update_projectiles(dt)
        self.__particle_controller.update_particles(dt)

        # reset frame
        self.__draw_screen = Surface(draw_screen_size // zoom)
        self.__ui_texture = Surface(draw_screen_size // zoom, SRCALPHA)
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())

        # drawing soldiers and their health bars
        for soldier in self.__soldier_tracker.get_soldiers():
            self.__draw_object_rt(soldier)

        # drawing turrets
        for turret in self.__turret_tracker.get_turrets():    
            self.__draw_object_rt(turret)

        # drawing farms
        for farm in self.__farm_tracker.get_farms():
            self.__draw_object_rt(farm)

        #drawing projectiles
        for projectile in self.__projectile_tracker.get_projectiles():
            texture = self.__assets["projectiles"]["arrow"]
            size = texture.get_size()
            self.__draw(
                texture,
                projectile.cords + \
                Vector2(TILE_SIZE // 2, TILE_SIZE - size[1]) \
                - Vector2(size[0], 0) // 2
            )
        # drawing particles
        for particle in self.__particle_controller.get_particles():
            self.__draw_particle(particle)
        
        self.__draw_screen.blit(self.__ui_texture, (0, 0))

        return scale(self.__draw_screen, Vector2(self.__draw_screen.get_size()) * zoom)

    def __draw_object_rt(self, object: ObjectRT):
        
        if object.__class__ == SoldierRT:
            direction = {
                (0, 0):    'bot',
                (0, -1):   'top',
                (0, 1):    'bot',
                (-1, 0):   'left',
                (1, 0):    'right'
            }[(int(object.direction.x), int(object.direction.y))]

            texture = self.__assets['soldiers'][object.name] \
            [object.animation][direction][object.frame]
        elif object.__class__ == FarmRT:
            texture = self.__assets["farms"]["farm"]
        elif object.__class__ == TurretRT:
            texture = self.__assets["turrets"]["turret"]            

        size = texture.get_size()

        self.__draw(
            texture,
            object.cords + \
            Vector2(TILE_SIZE // 2, TILE_SIZE - size[1]) \
            - Vector2(size[0], 0) // 2
        )
        
        if object.__class__ == SoldierRT:
            size = texture.get_size()[0] // 2
            bar = Surface((size, 1))
            bar.fill((255, 0, 0))
            self.__draw(bar, object.cords - Vector2(-1, 4))

            bar = Surface((object.actual_hp_rate * size, 1))
            bar.fill((0, 255, 0))
            self.__draw(bar, object.cords - Vector2(-1, 4))

        if object.view_rate[0] > 0:

            infos = object.stats
            text_surfaces = [
                self.__font_renderer.render(f'{name}: {info}', 'small')
                for name, info in infos.items()
            ]

            info_tab_size = Vector2(
                max(s.get_size()[0] for s in text_surfaces) + INFO_TAB_MARGIN * 2,
                sum((s.get_size()[1] for s in text_surfaces)) + INFO_TAB_MARGIN * 2,
            )

            info_tab = Surface(info_tab_size, SRCALPHA)

            info_tab.fill((0, 0, 0, 120))
            [
                info_tab.blit(s.subsurface(Rect(0, 0, object.view_rate[4 + i] * s.get_size()[0], s.get_size()[1])), (INFO_TAB_MARGIN, INFO_TAB_MARGIN + sum(s.get_size()[1] for s in text_surfaces[:i])))
                for i, s in enumerate(text_surfaces)
            ]

            draw_rect(info_tab, (0, 0, 0, 0), Rect(
                0, info_tab_size.y * object.view_rate[4] + 1, 
                info_tab_size.x,
                info_tab_size.y
            ))

            draw_points = (
                Vector2(0, 1),
                Vector2(info_tab_size.x + 1, 1),
                Vector2(info_tab_size.x + 1, -info_tab_size.y),
                Vector2(0, -info_tab_size.y),
                Vector2(0, 0),
            )
            
            for i in range(1, len(draw_points)):
                if object.view_rate[i - 1] > 0:
                    self.__draw_line(
                        object.cords - draw_points[i - 1],
                        object.cords - draw_points[i],
                        Color(255, 255, 255),
                        object.view_rate[i - 1],
                        True
                    )
            
            if object.view_rate[4] > 0:
                self.__draw(
                    info_tab,
                    object.cords - Vector2(info_tab.get_size()[0], 0),
                    True
                )

        # real pos
        if SHOW_REAL_POS:
            surf = Surface((1, 1))
            surf.fill((255, 0, 0))
            self.__draw(surf, object.cords)

    def __draw_particle(self, particle: Particle):
        pos, color, size = particle.get_data()
        surf = Surface((size, size), SRCALPHA)
        surf.fill(color)
        self.__draw(surf, pos)
    
    def __draw_line(self, pos1: Vector2, pos2: Vector2, color: Color, len: float = 1, ui: bool = False):
        '''Draw line with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        pos2_real = pos1.move_towards(pos2, pos1.distance_to(pos2) * len)

        size = Vector2(
            abs(pos1.x - pos2_real.x),
            abs(pos1.y - pos2_real.y),
        )

        if all((
            -size.x <= pos1.x + self.__camera.get_offset().x <= self.__draw_screen.get_size()[0],
            -size.y <= pos1.y + self.__camera.get_offset().y <= self.__draw_screen.get_size()[1], 
            -size.x <= pos2_real.x + self.__camera.get_offset().x <= self.__draw_screen.get_size()[0],
            -size.y <= pos2_real.y + self.__camera.get_offset().y <= self.__draw_screen.get_size()[1],
        )):
            draw_line(self.__ui_texture if ui else self.__draw_screen, color, pos1 + self.__camera.get_offset(), pos2_real + self.__camera.get_offset())

    def __draw(self, texture: Surface, pos: Vector2, ui: bool = False) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if all((
            -size.x <= pos.x + self.__camera.get_offset().x <= self.__draw_screen.get_size()[0],
            -size.y <= pos.y + self.__camera.get_offset().y <= self.__draw_screen.get_size()[1],
        )):
            if ui:
                self.__ui_texture.blit(texture, pos + self.__camera.get_offset())
            else:
                self.__draw_screen.blit(texture, pos + self.__camera.get_offset())
from pygame import Vector2, Surface, Rect, Color, SRCALPHA, transform
from pygame.draw import rect as draw_rect, line as draw_line
from packages.gui.const import TILE_SIZE, SHOW_REAL_POS, HEALTH_BAR_COLOR_BACK, \
    HEALTH_BAR_COLOR_FRONT, HEALTH_BAR_SIZE, INFO_TAB_SHOW_TIME, \
    INFO_TAB_SHOW_SMOOTH, INFO_TAB_MARGIN
from .objects_rt.object_rt import ObjectRT
from .objects_rt.farm_rt import FarmRT
from .objects_rt.turret_rt import TurretRT
from .objects_rt.soldier_rt import SoldierRT
from .objects_rt.obstacle_rt import ObstacleRT

from .font_renderer import FontRenderer
from .particle import Particle
from .projectile import Projectile
from .map_renderer import MapRenderer

class Draw:
    def __init__(self, assets, game) -> None:
        self.__assets = assets
        self.__camera_offset = Vector2()
        self.__font_renderer = FontRenderer()
        self.__draw_screen = None
        self.__map_renderer = MapRenderer()
        self.__map_texture = self.__map_renderer.render(self.__assets, game)
    
    def begin(self, camera_offset: Vector2, size):
        self.__camera_offset = camera_offset
        self.__draw_screen = Surface(size)
        self.__ui_texture = Surface(size, SRCALPHA)
        self.__draw_screen.blit(self.__map_texture, self.__camera_offset)

    def end(self) -> Surface:
        self.__draw_screen.blit(self.__ui_texture, (0, 0))
        return self.__draw_screen

    def projectile(self, projectile: Projectile):
            texture = self.__assets["projectiles"]["arrow"]
            self.draw(
                transform.rotate(texture, projectile.angle),
                projectile.pos + Vector2(TILE_SIZE) // 2
            )

    def object_rt(self, object: ObjectRT):
        
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

            self.__health_bar(object)

        elif object.__class__ == FarmRT:
            texture = self.__assets["farms"]["farm"]
        elif object.__class__ == TurretRT:
            texture = self.__assets["turrets"]["turret"]
        elif object.__class__ == ObstacleRT:
            texture = self.__assets["obstacles"]["obstacle_" + object.name]
        else:
            raise Exception(f'{object} is not a real time object!')        

        size = texture.get_size()

        self.draw(texture,
             object.cords + Vector2((TILE_SIZE - size[0]) // 2, TILE_SIZE - size[1]))
            
        self.info_bar(
            object.stats, object.cords,
            object.select_time / INFO_TAB_SHOW_TIME
        )

        # real pos
        if SHOW_REAL_POS:
            surf = Surface((1, 1))
            surf.fill((255, 0, 0))
            self.draw(surf, object.cords)

    def __health_bar(self, soldier: SoldierRT):
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
        self.draw(
            bar,
            soldier.cords + Vector2(TILE_SIZE - HEALTH_BAR_SIZE[0], -1) // 2
        )
    
    def info_bar(self, info: dict[str, str], pos: Vector2, animation_progress: float):
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
            return (x / (b * 1.01) - int(x / (b * 1.01))) ** (1 / A)

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

            direction = pos.x - size.x + self.__camera_offset.x > 0

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
                    self.line(
                        pos + frame_offset + draw_points[i - 1],
                        pos + frame_offset + draw_points[i],
                        Color(255, 255, 255),
                        view_rate[i - 1],
                        True
                    )
            
            tab_offset = Vector2(-size.x, 0) if direction else Vector2(TILE_SIZE, 0)

            if view_rate[4] > 0:
                self.draw(
                    info_tab,
                    pos + tab_offset ,
                    True
                )

    def particle(self, particle: Particle):
        '''Draws particle.
        '''

        pos, color, size = particle.get_data()
        surf = Surface((size, size), SRCALPHA)
        surf.fill(color)
        self.draw(surf, pos)
    
    def line(self, pos1: Vector2, pos2: Vector2, color: Color,
            len: float = 1, ui: bool = False):
        '''Draw line with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        pos2_real = pos1.move_towards(pos2, pos1.distance_to(pos2) * len)

        size = Vector2(
            abs(pos1.x - pos2_real.x),
            abs(pos1.y - pos2_real.y),
        )
        
        ca = self.__camera_offset
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

    def draw(self, texture: Surface, pos: Vector2, ui: bool = False) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        ca = self.__camera_offset
        dss = self.__draw_screen.get_size()

        size = Vector2(texture.get_size())
        if all((
            -size.x <= pos.x + ca.x <= dss[0],
            -size.y <= pos.y + ca.y <= dss[1],
        )):
            if ui: self.__ui_texture.blit(texture, pos + ca)
            else: self.__draw_screen.blit(texture, pos + ca)
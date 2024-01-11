from .gui_object import GUIobject
from pygame import Surface, Rect
from pygame.event import Event
from pygame.image import load
from pygame.transform import scale
from pygame import Vector2
from .gui_element import GUIElement
from packages import ASSETS_DIRECTORY
from pygame.draw import rect as draw_rect
from packages.gui.const import HEADER_BAR_SIZE, BORDER_SIZE, HEADER_BAR_PADDING, GUI_COLORS

class Window(GUIobject):
    def __init__(self, sub_objects: list[GUIobject], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        kwargs['font_size'] = int(HEADER_BAR_SIZE // 2)
        super().__init__(sub_objects, pos, size, **kwargs)
        if 'icon' in self.properties:
            self.icon = scale(
                load(f'{ASSETS_DIRECTORY}/textures/icons/{self.properties["icon"]}.png'),
                Vector2(HEADER_BAR_SIZE / 1.5)
            )

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('background_color', GUI_COLORS['background1']))
        if 'name' in self.properties:
            border_color = self.properties.get('border_color', GUI_COLORS['window_border'])
            if 'headerbar_color' in self.properties:
                surf.fill(
                    self.properties['headerbar_color'], 
                    Rect(0, 0, self.real_size.x, HEADER_BAR_SIZE)
                )
            draw_rect(
                surf,
                border_color,
                Rect(0, 0, self.real_size.x, self.real_size.y), width=BORDER_SIZE
            )
            draw_rect(
                surf,
                border_color,
                Rect(0, 0, self.real_size.x, HEADER_BAR_SIZE), width=BORDER_SIZE
            )
            if 'icon' in self.properties:
                surf.blit(self.icon, (HEADER_BAR_PADDING, (HEADER_BAR_SIZE - self.icon.get_size()[1]) // 2))
                offset = self.icon.get_size()[0]
            else:
                offset = 0
            text = self.font.render(
                str.capitalize(self.properties.get('name', "")),
                True,
                self.properties.get('header_color', (255, 255, 255))
            )
            surf.blit(text, (HEADER_BAR_PADDING * 2 + offset, (HEADER_BAR_SIZE - text.get_size()[1]) // 2))
        for object in self.sub_objects:
            surf.blit(object.render(), object.real_pos)
        return surf
    
    def calc_pos(self):
        for object in self.sub_objects:
            object.real_pos = Vector2(
                self.real_size.x * object.pos.x,
                ((self.real_size.y - HEADER_BAR_SIZE) * object.pos.y + HEADER_BAR_SIZE)
                if 'name' in self.properties else
                self.real_size.y * object.pos.y
            )

            object.real_size = Vector2(
                self.real_size.x * object.size.x,
                (self.real_size.y - HEADER_BAR_SIZE) * object.size.y
                if 'name' in self.properties else
                self.real_size.y * object.size.y,
            )

            object.global_pos = self.global_pos + object.real_pos

    def handle_event(self, event: Event) -> None:
        for object in self.sub_objects:
            object.handle_event(event)

    def update(self, dt) -> None:
        for object in self.sub_objects:
            object.update(dt)
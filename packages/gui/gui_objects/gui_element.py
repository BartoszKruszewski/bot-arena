from abc import ABC
from .gui_object import GUIobject
from pygame.event import Event
from pygame import Surface, font, MOUSEBUTTONDOWN, BUTTON_LEFT, SRCALPHA, Rect
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect as draw_rect
from packages.gui.const import GUI_COLORS, ROUNDED_RADIUS, MAX_HOVER_TIME

def easeInOutCubic(x):
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

class GUIElement(GUIobject, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)
        self.hover_time = 0
        self.properties['hover_intense'] = 0

    def handle_event(self, event):
        pass
            
    def update(self, dt):
        if self.in_mouse_range():
            self.hover_time += dt
        else:
            self.hover_time -= dt
        self.hover_time = min(max(self.hover_time, 0), MAX_HOVER_TIME)
        self.properties['hover_intense'] = easeInOutCubic(self.hover_time / MAX_HOVER_TIME)

    def render(self) -> Surface:
        surf = Surface(self.real_size, SRCALPHA)
        background_color = self.properties.get('background_color', GUI_COLORS['none'])
        rounded_radius = self.properties.get('rounded', ROUNDED_RADIUS)
        if rounded_radius > 0:
            draw_rect(
                surf,
                background_color,
                Rect(0, 0, self.real_size.x, self.real_size.y),
                border_radius = rounded_radius
            )
        else:
            surf.fill(background_color)
        text = self.font.render(
            self.properties.get('text', ""),
            True,
            self.properties.get('text_color', GUI_COLORS['text']))
        surf.blit(text, (
            (self.real_size.x - text.get_size()[0]) // 2,
            (self.real_size.y - text.get_size()[1]) // 2,
        ))
        return surf

    def is_clicked(self, event: Event) -> bool:
        if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
            return self.in_mouse_range()
        return False

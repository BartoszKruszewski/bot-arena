from abc import ABC
from .gui_object import GUIobject
from pygame.event import Event
from pygame import Surface, font, MOUSEBUTTONDOWN, BUTTON_LEFT, SRCALPHA, Rect
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect as draw_rect
from packages.gui.const import GUI_COLORS, ROUNDED_RADIUS

class GUIElement(GUIobject, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self) -> Surface:
        surf = Surface(self.real_size, SRCALPHA)
        background_color = self.properties.get('background_color', GUI_COLORS['none'])
        if 'rounded' in self.properties:
            draw_rect(
                surf,
                background_color,
                Rect(0, 0, self.real_size.x, self.real_size.y),
                border_radius=ROUNDED_RADIUS
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

    def in_mouse_range(self, event_or_none: Event = None) -> bool:
        if event_or_none is None:
            mouse_pos = get_pos()
        else:
            if event_or_none.type != MOUSEBUTTONDOWN:
                raise Exception("Event type is not MOUSEBUTTONDOWN")
            mouse_pos = event_or_none.pos
        return all((
            self.global_pos.x < mouse_pos[0] < self.global_pos.x + self.real_size.x,
            self.global_pos.y < mouse_pos[1] < self.global_pos.y + self.real_size.y
        )) 

    def is_clicked(self, event: Event) -> bool:
        if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
            return self.in_mouse_range(event)
        return False

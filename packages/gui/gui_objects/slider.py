from .gui_element import GUIElement
from .window import Window
from .scene import Scene
from .button import Button
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, BUTTON_LEFT, BLEND_RGBA_ADD, SRCALPHA
from pygame.event import Event as pgevent, Event
from pygame import Surface
from packages.gui.const import GUI_COLORS

class Slider(Button):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['is_dragged'] = False
        self.properties['slider'] = None

    def handle_event(self, event: Event) -> None:
        if self.is_clicked(event):
            self.properties['is_dragged'] = True
        if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
            self.properties['is_dragged'] = False

        if self.properties['is_dragged']:
            where = (event.pos[0] - self.global_pos.x) / self.real_size.x
            where = min(max(where, 0), 1)

            where = min(max(where, 0.05), 0.953)
            self.properties['slider']['pos'] = (where * self.real_size.x - self.properties['slider']['size'][0] / 2, 0)

            def map_range(x, min_in, max_in, min_out=0, max_out=1):
                return (x - min_in) * (max_out - min_out) / (max_in - min_in) + min_out
            
            self.properties.get('on_change', lambda x: None)(map_range(where, 0.05, 0.953))
            
    def render(self):
        surf = super().render()
        if self.properties['slider'] is None:
            slider_size = (self.real_size.x / 10, self.real_size.y)
            slider_pos = (self.real_size.x / 2 - slider_size[0] / 2, 0)
            self.properties['slider'] = {'size': slider_size, 'pos': slider_pos}

        slider_surf = Surface(self.properties['slider']['size'], SRCALPHA)
        slider_surf.fill((*GUI_COLORS['button'], 0))
        surf.blit(slider_surf, self.properties['slider']['pos'], special_flags=BLEND_RGBA_ADD)

        return surf

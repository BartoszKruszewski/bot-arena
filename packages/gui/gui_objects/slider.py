from .gui_element import GUIElement
from .window import Window
from .scene import Scene
from .button import Button
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, BUTTON_LEFT, BLEND_RGBA_ADD, SRCALPHA
from pygame.event import Event as pgevent, Event
from pygame import Surface
from packages.gui.const import GUI_COLORS

def color_blend(c1, c2, w):
    return (
        c1[0] * (1 - w) + c2[0] * w,
        c1[1] * (1 - w) + c2[1] * w,
        c1[2] * (1 - w) + c2[2] * w,
    )

class Slider(Button):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['is_dragged'] = False
        self.properties['slider'] = None
        self.properties['background_color_hovered'] = GUI_COLORS['button']
        self.properties['update_slider_pos'] = self.update_slider_pos

    def handle_event(self, event: Event) -> None:
        if self.is_clicked(event):
            self.properties['is_dragged'] = True
        if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
            self.properties['is_dragged'] = False

        if self.properties['is_dragged']:
            where = (event.pos[0] - self.global_pos.x) / self.real_size.x
            where = min(max(where, 0.05), 0.953)
            self.properties['slider']['pos'] = (where * self.real_size.x - self.properties['slider']['size'][0] / 2, 0)

            def map_range(x, min_in, max_in, min_out=0, max_out=1):
                return (x - min_in) * (max_out - min_out) / (max_in - min_in) + min_out
            
            self.properties.get('on_change', lambda x: None)(map_range(where, 0.05, 0.953))
    
    def update_slider_pos(self, value):
        where = min(max(value, 0.05), 0.953) 
        self.properties['slider']['pos'] = (where * self.real_size.x - self.properties['slider']['size'][0] / 2, 0)

    def render(self):
        surf = super().render()
        if self.properties['slider'] is None:
            slider_size = (self.real_size.x / 10, self.real_size.y)
            slider_pos = (self.real_size.x / 2 - slider_size[0] / 2, 0)
            self.properties['slider'] = {'size': slider_size, 'pos': slider_pos}

        slider_surf = Surface(self.properties['slider']['size'], SRCALPHA)
        color = color_blend(
                self.standard_color,
                self.properties.get('slider_color_hovered', GUI_COLORS['button_hovered']), 
                self.properties['hover_intense']
            )
        slider_surf.fill((*color, 0))
        surf.blit(slider_surf, self.properties['slider']['pos'], special_flags=BLEND_RGBA_ADD)

        return surf

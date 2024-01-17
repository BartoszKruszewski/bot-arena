from .gui_element import GUIElement
from pygame.event import Event
from packages.gui.const import GUI_COLORS
from pygame import Color

def color_blend(c1, c2, w):
    return (
        c1[0] * (1 - w) + c2[0] * w,
        c1[1] * (1 - w) + c2[1] * w,
        c1[2] * (1 - w) + c2[2] * w,
    )

class Button(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.on_click = self.properties.get('on_click', lambda: None)
        self.properties['blocked'] = self.properties.get('blocked', False)
        self.standard_color = self.properties.get('background_color', GUI_COLORS['button']) 

    def handle_event(self, event: Event) -> None:
        if not self.properties.get('blocked', False):
            if self.is_clicked(event):
                self.on_click(*self.properties.get('args', ()))

    def render(self):
        if self.properties['blocked']:
            self.properties['background_color'] = \
                self.properties.get('blocked_color', GUI_COLORS['blocked'])
        else:
            self.properties['background_color'] = color_blend(
                self.standard_color,
                self.properties.get('background_color_hovered', GUI_COLORS['button_hovered']), 
                self.properties['hover_intense']
            )
            self.properties['text_color'] = color_blend(
                GUI_COLORS['text'], self.standard_color, self.properties['hover_intense'])
        return super().render()
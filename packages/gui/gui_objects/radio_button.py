from .gui_element import GUIElement
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event as pgevent, Event
from packages.gui.const import GUI_COLORS

def color_blend(c1, c2, w):
    if len(c1) == 3:
        c1 = (c1[0], c1[1], c1[2], 255)
    if len(c2) == 3:
        c2 = (c2[0], c2[1], c2[2], 255)
    return (
        c1[0] * (1 - w) + c2[0] * w,
        c1[1] * (1 - w) + c2[1] * w,
        c1[2] * (1 - w) + c2[2] * w,
        c1[3] * (1 - w) + c2[3] * w
    )

class RadioButton(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['active'] = self.properties.get('active', False)
        self.properties['blocked'] = self.properties.get('blocked', False)
        self.on_click = self.properties.get('on_click', lambda: None)
        self.standard_color = self.properties.get('background_color', GUI_COLORS['button'])      

    def handle_event(self, event: Event) -> None:
        if not self.properties['blocked']:
            if self.is_clicked(event):
                self.properties['active'] = not self.properties['active']
                self.on_click()

    def update(self, dt):
        super().update(dt)
        if self.properties['active']:
            self.properties['text_color'] = self.properties.get('edit_text_color', GUI_COLORS['background2'])
        else:
            self.properties['text_color'] = self.properties.get('main_text_color', GUI_COLORS['text'])

    def render(self):
        if self.properties['blocked']:
            self.properties['background_color'] = \
                self.properties.get('blocked_color', GUI_COLORS['blocked'])
        elif self.properties['active']:
            self.properties['background_color'] = \
                self.properties.get('active_color', GUI_COLORS['active'])
        else:
            self.properties['background_color'] = color_blend(
                self.standard_color, GUI_COLORS['button_hovered'], self.properties['hover_intense'])
            self.properties['text_color'] = color_blend(
                GUI_COLORS['text'], self.standard_color, self.properties['hover_intense'])
        return super().render()


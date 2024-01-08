from .gui_element import GUIElement
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event as pgevent, Event
from packages.gui.const import GUI_COLORS

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

    def render(self):
        if self.properties['blocked']:
            self.properties['background_color'] = \
                self.properties.get('blocked_color', GUI_COLORS['blocked'])
        elif self.properties['active']:
            self.properties['background_color'] = \
                self.properties.get('active_color', GUI_COLORS['active'])
        else:
            self.properties['background_color'] = self.standard_color
        return super().render()


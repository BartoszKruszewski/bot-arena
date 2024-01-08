from .gui_element import GUIElement
from pygame.event import Event
from packages.gui.const import GUI_COLORS

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
            self.properties['background_color'] = self.standard_color
        return super().render()
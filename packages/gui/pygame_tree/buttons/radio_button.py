from ..gui_object import GUIElement
from pygame import MOUSEBUTTONDOWN, Surface
from pygame.event import Event as pgevent

class RadioButton(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['active'] = self.properties.get('active', False)

        self.on_click = self.properties.get('on_click', lambda: None)
        self.active_color = self.properties.get('active_color', (255, 255, 255))
        self.color = self.properties.get('color', (0, 0, 0))

    def handle_event(self, event: pgevent) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if self.global_pos.x < event.pos[0] < self.global_pos.x + self.real_size.x:
                if self.global_pos.y < event.pos[1] < self.global_pos.y + self.real_size.y:
                    self.properties['active'] = not self.properties['active']
                    self.on_click()
                    
    def render(self, dt, mouse) -> Surface:
        self.properties['color'] = self.active_color if self.properties['active'] else self.color
        return super().render(dt, mouse)

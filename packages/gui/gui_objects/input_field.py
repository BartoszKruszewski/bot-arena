from .radio_button import RadioButton
from pygame import Surface, font, KEYDOWN, K_BACKSPACE, event as pgevent

class InputField(RadioButton):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['value'] = self.properties.get('value', '')

        self.filter = self.properties.get('filter', lambda x: True)

    def handle_event(self, event: pgevent):
        super().handle_event(event)

        if event.type == KEYDOWN and self.properties['active']:
            if event.key == K_BACKSPACE:
                self.properties['value'] = self.properties['value'][:-1]
            else:
                new_text = self.properties['value'] + event.unicode
                if self.filter(new_text):
                    self.properties['value'] = new_text
            
    def render(self) -> Surface:
        surf = super().render()
        surf.blit(
            font.SysFont('arial', 30).render(self.properties['value'], True, (0, 0, 0)),
            (self.real_size.x / 2 - 30, self.real_size.y / 2 - 15)
        )
        return surf
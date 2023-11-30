from .radio_button import RadioButton
from pygame import Surface, font, KEYDOWN, K_BACKSPACE, event as pgevent

class InputField(RadioButton):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['text'] = self.properties.get('text', '')

        self.filter = self.properties.get('filter', lambda x: True)

    def handle_event(self, event: pgevent):
        super().handle_event(event)

        if event.type == KEYDOWN and self.properties['active']:
            if event.key == K_BACKSPACE:
                self.properties['text'] = self.properties['text'][:-1]
            else:
                new_text = self.properties['text'] + event.unicode
                if self.filter(new_text):
                    self.properties['text'] = new_text
from .radio_button import RadioButton
from pygame import Surface, font, KEYDOWN, K_BACKSPACE, event as pgevent, MOUSEBUTTONDOWN
from packages.gui.const import GUI_COLORS

class InputField(RadioButton):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['default'] = str(kwargs.get('default', '...'))
        self.properties['text'] = self.properties['default']

        self.filter = self.properties.get('filter', lambda x: True)

    def handle_event(self, event: pgevent):
        super().handle_event(event)

        if event.type == MOUSEBUTTONDOWN:
            self.properties['active'] = self.in_mouse_range()

        if event.type == KEYDOWN and self.properties['active']:
            if event.key == K_BACKSPACE:
                self.properties['text'] = self.properties['text'][:-1]
                self.properties['when_type']()
            else:
                new_text = ('' if self.properties['text'] == self.properties['default'] else self.properties['text']) + event.unicode
                if self.filter(new_text):
                    self.properties['text'] = new_text
                    self.properties['when_type']()

                    

    def update(self, dt):
        super().update(dt)

        if not self.properties['active']:
            if self.properties['text'] == self.properties['default']:
                self.properties['text_color'] = self.properties.get('default_color', GUI_COLORS['button'])
            else:
                self.properties['text_color'] = self.properties.get('active_color', GUI_COLORS['active'])

        
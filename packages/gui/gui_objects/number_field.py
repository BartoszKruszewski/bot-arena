from .input_field import InputField
from .gui_object import GUIobject
from .window import Window
from .button import Button
from packages.gui.const import GUI_COLORS

class NumberField(Window):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(
            [
                Button(
                    (0, 0.1), (0.2, 0.8),
                    background_color = GUI_COLORS['button'],
                    on_click = self.decrement,
                    rounded = 20,
                    text = '-',
                    text_color = GUI_COLORS['background2']

                ),
                InputField(
                    (0.2 + 0.05, 0), (1 - 2 * 0.2 - 0.1, 1),
                    default = str(kwargs.get('default', 0)),
                    filter = self.number_filter,
                    id = str(self),
                    rounded = 10,
                    background_color = GUI_COLORS['background2'],
                ),
                Button(
                    (1 - 0.2, 0.1), (0.2, 0.8),
                    background_color = GUI_COLORS['button'],
                    on_click = self.increment,
                    rounded = 20,
                    text = '+',
                    text_color = GUI_COLORS['background2']
                )
            ], pos, size, **kwargs)
        
        self.properties['default'] = str(kwargs.get('default', 0))
        self.properties['interval'] = self.properties.get('interval', 1)
        self.properties['minimum'] = self.properties.get('minimum', None)
        self.properties['maximum'] = self.properties.get('maximum', None)
        
    def number_filter(self, text):
        return text.isnumeric() and int(text) < self.properties['maximum']

    def increment(self):
        text = self.get_info(str(self), 'text')
        if text == '':
            text = '0'
        number = int(text) + self.properties['interval']
        if self.properties['minimum'] is not None:
            number = max(self.properties['minimum'], number)
        if self.properties['maximum'] is not None:
            number = min(self.properties['maximum'], number)
        self.send_info(str(self), 'text', str(number))
        self.send_info(str(self), 'active', False)

    def decrement(self):
        text = self.get_info(str(self), 'text')
        if text == '':
            text = '0'
        number = int(text) - self.properties['interval']
        if self.properties['minimum'] is not None:
            number = max(self.properties['minimum'], number)
        if self.properties['maximum'] is not None:
            number = min(self.properties['maximum'], number)
        self.send_info(str(self), 'text', str(number))
        self.send_info(str(self), 'active', False)

    def update(self, dt):
        super().update(dt)
        self.properties['text'] = self.sub_objects[1].properties['text']
        if not self.sub_objects[1].properties['active']:
            if self.sub_objects[1].properties['text'] == self.properties['default']:
                self.sub_objects[1].properties['text_color'] = self.properties.get('default_color', GUI_COLORS['button'])
            else:
                self.sub_objects[1].properties['text_color'] = self.properties.get('active_color', GUI_COLORS['active'])
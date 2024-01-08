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
                    (0, 0), (0.3, 1),
                    background_color = GUI_COLORS['text'],
                    on_click = self.decrement,
                    rounded = 3,
                    text = '-',
                    text_color = GUI_COLORS['background2']

                ),
                InputField(
                    (0.3, 0), (0.4, 1),
                    text = str(kwargs.get('default', 0)),
                    filter = self.number_filter,
                    id = str(self),
                    rounded = 0,
                    
                ),
                Button(
                    (0.7, 0), (0.3, 1),
                    background_color = GUI_COLORS['text'],
                    on_click = self.increment,
                    rounded = 3,
                    text = '+',
                    text_color = GUI_COLORS['background2']
                )
            ], pos, size, **kwargs)
        
        self.properties['interval'] = self.properties.get('interval', 1)
        self.properties['minimum'] = self.properties.get('minimum', None)
        self.properties['maximum'] = self.properties.get('maximum', None)
        
    def number_filter(self, text):
        return text.isnumeric() and int(text) < self.properties['maximum']

    def increment(self):
        number = int(self.get_info(str(self), 'text')) + self.properties['interval']
        if self.properties['minimum'] is not None:
            number = max(self.properties['minimum'], number)
        if self.properties['maximum'] is not None:
            number = min(self.properties['maximum'], number)
        self.send_info(str(self), 'text', str(number))
        self.send_info(str(self), 'active', False)

    def decrement(self):
        number = int(self.get_info(str(self), 'text')) - self.properties['interval']
        if self.properties['minimum'] is not None:
            number = max(self.properties['minimum'], number)
        if self.properties['maximum'] is not None:
            number = min(self.properties['maximum'], number)
        self.send_info(str(self), 'text', str(number))
        self.send_info(str(self), 'active', False)

    def update(self, dt):
        self.properties['text'] = self.sub_objects[1].properties['text']
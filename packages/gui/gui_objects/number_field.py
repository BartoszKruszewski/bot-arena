from .input_field import InputField
from .gui_object import GUIobject
from .window import Window
from .button import Button

class NumberField(Window):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(
            [
                Button(
                    (0, 0), (0.2, 1),
                    color = (20,20,20),
                    on_click = self.decrement
                ),
                InputField(
                    (0.2, 0), (0.60, 1),
                    color = (200, 200, 200),
                    text = str(kwargs.get('default', 0)),
                    filter = self.number_filter,
                    id = str(self) # !!!!!!!!!!!!!!!!!!!!
                ),
                Button(
                    (0.8, 0), (0.2, 1),
                    color = (100,100,100),
                    on_click = self.increment
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
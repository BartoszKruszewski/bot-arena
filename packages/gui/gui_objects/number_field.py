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
                    value = '0',
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
        
        
    def number_filter(self, text):
        if not text.isnumeric():
            return False
        return True

    def increment(self):
        number = str(int(self.get_info(str(self), 'value')) + self.properties['interval'])
        self.send_info(str(self), 'value', number)
        self.send_info(str(self), 'active', False)
        print("chuj")

    def decrement(self):
        number = str(int(self.get_info(str(self), 'value')) - self.properties['interval'])
        self.send_info(str(self), 'value', number)
        self.send_info(str(self), 'active', False)

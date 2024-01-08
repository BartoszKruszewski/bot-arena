from .radio_button import RadioButton
from .window import Window
from packages.gui.const import GUI_COLORS

class List(Window):
    def __init__(self, objects_in_list: list[str], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)
        button_size = self.properties.get('button_size', (0.9, 0.1))
        gap = self.properties.get('gap', (0.05, 0.01))
        self.properties['max_active'] = kwargs.get('max_active', len(objects_in_list))
        self.sub_objects = [
            RadioButton(
                (gap[0], i * (button_size[1] + gap[1])), (button_size[0], button_size[1]),
                background_color = self.properties.get('element_color', GUI_COLORS['none']),
                active_color=self.properties.get('active_element_color', GUI_COLORS['active']),
                on_click = lambda: self.properties.get('on_click', lambda: None)(self.get_active()),
                text = object,
            )
            for i, object in enumerate(objects_in_list)]

    def get_active(self):
        active_buttons = [
            button.properties['text']
            for button in self.sub_objects
            if button.properties['active']
        ]
        if len(active_buttons) == self.properties['max_active']:
            for button in self.sub_objects:
                if not button.properties['active']:
                    button.properties['blocked'] = True
        else:
            for button in self.sub_objects:
                button.properties['blocked'] = False
        return active_buttons
        



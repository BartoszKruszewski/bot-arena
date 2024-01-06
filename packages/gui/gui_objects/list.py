from .radio_button import RadioButton
from .window import Window

class List(Window):
    def __init__(self, objects_in_list: list[str], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)
        interval = 1 / len(objects_in_list)
        self.properties['max_active'] = kwargs.get('max_active', len(objects_in_list))
        self.sub_objects = [
            RadioButton(
                (0, i * interval), (1, interval),
                color=(255, 0, 0),
                active_color=(0, 255, 0),
                on_click = lambda: self.properties.get('on_click', lambda: None)(self.get_active()),
                fontSize = 12,
                text = object
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
        



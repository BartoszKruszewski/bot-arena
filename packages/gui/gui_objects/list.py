from .radio_button import RadioButton
from .window import Window

class List(Window):
    def __init__(self, sub_objects_str: list[str], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)
        interval = 1 / len(sub_objects_str)
        self.sub_objects = [
            RadioButton(
                (i * interval, 0), (interval, 1),
                color=(255, 0, 0),
                active_color=(0, 255, 0),
                on_click=self.generate_function(self.properties.get("on_click", lambda:None), i),
                fontSize = 12,
                text = sub_objects_str[i]
            )
            for i in range(len(sub_objects_str))]

    def generate_function(self, on_click, index : int):
        return lambda: on_click(index)


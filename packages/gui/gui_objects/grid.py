from .list import List
from .radio_button import RadioButton
from .window import Window

class Grid(Window):
    def __init__(self, sub_objects_str: list[str], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)
        interval = 1 / len(sub_objects_str)
        self.sub_objects = [
            List(
                sub_objects_str[i],
                (0, i * interval), (1, interval),
                color=self.properties.get('color', (255, 0, 0)),
                on_click=self.generate_function(self.properties.get("on_click", lambda:None), i)
            )
            for i in range(len(sub_objects_str))]
            
    def generate_function(self, on_click, y : int):
        return lambda x: on_click(x, y)


from .button import Button
from .window import Window

class TimeController(Window):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__([], pos, size, **kwargs)

        self.properties.get("prev_on_click", lambda:None)
        self.properties.get("play_on_click", lambda:None)
        self.properties.get("next_on_click", lambda:None)

        self.sub_objects = [
            Button(
                (0, 0), (0.3, 1),
                color=(255, 0, 0),
                on_click=self.properties.get("prev_on_click", lambda:None),
                fontSize = 12,
                text = "   <"
            ),
            Button(
                (0.35, 0), (0.3, 1),
                color=(0, 255, 0),
                on_click=self.properties.get("play_on_click", lambda:None),
                fontSize = 12,
                text = "   ||"
            ),
            Button(
                (0.7, 0), (0.3, 1),
                color=(255, 0, 0),
                on_click=self.properties.get("next_on_click", lambda:None),
                fontSize = 12,
                text = "   >"
            )
        ]



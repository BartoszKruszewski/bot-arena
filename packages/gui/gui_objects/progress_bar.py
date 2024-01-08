from pygame import Surface, Rect, BLEND_RGB_ADD
from .gui_element import GUIElement
from packages.gui.const import GUI_COLORS

class ProgressBar(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], **kwargs):
        super().__init__(pos, size, **kwargs)
        self.properties['state'] = 0
        self.properties['background_color'] = self.properties.get('background_color', GUI_COLORS['blocked'])

    def render(self) -> Surface:
        surf = super().render()
        surf.fill(
            self.properties.get('color', GUI_COLORS['active']),
            Rect(
                0, 0,
                self.properties['state'] * self.real_size.x,
                self.real_size.y
            ), special_flags=BLEND_RGB_ADD)
        return surf
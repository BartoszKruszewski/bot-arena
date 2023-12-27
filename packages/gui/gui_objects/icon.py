from pygame.image import load
from pygame.transform import scale
from pygame import Vector2
from .gui_element import GUIElement
from packages import ASSETS_DIRECTORY

class Icon(GUIElement):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], icon_name: str, **kwargs):
        super().__init__(pos, size, **kwargs)
        self.surf = load(f'{ASSETS_DIRECTORY}/textures/icons/{icon_name}.png')

    def render(self):
        scale_size = Vector2(self.surf.get_size()) * (self.real_size.x // self.surf.get_size()[0])
        return scale(self.surf, scale_size)
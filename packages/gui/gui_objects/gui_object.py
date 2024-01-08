from pygame import Vector2, mouse
from abc import ABC
from packages import ASSETS_DIRECTORY
from pygame.font import Font
from packages.gui.const import STANDARD_FONT_SIZE

class GUIobject(ABC):
    def __init__(self, sub_objects: list['GUIobject'], pos: tuple[float, float], size: tuple[float, float], **kwargs):
        self.sub_objects = sub_objects

        self.pos = Vector2(pos)
        self.size = Vector2(size)

        self.real_pos = None 
        self.real_size = None
        self.global_pos = None
        self.properties = kwargs

        self.font = Font(
                f'{ASSETS_DIRECTORY}/{self.properties.get("font", "font_gui")}.ttf',
                self.properties.get('font_size', STANDARD_FONT_SIZE)
            )

    def get_info(self, id: str, property: str):
        if self.properties.get("id", None) == id:
            return self.properties.get(property, None)

        if self.sub_objects:
            for obj in self.sub_objects:
                info = obj.get_info(id, property)
                if info is not None: 
                    return info

        return None

    def send_info(self, id: str, property: str, info) -> bool:
        if self.properties.get("id", None) == id:
            self.properties[property] = info
            return True

        if self.sub_objects:
            for obj in self.sub_objects:
                state = obj.send_info(id, property, info)
                if state: return True

        return False
        
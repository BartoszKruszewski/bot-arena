from os import listdir
from pygame.image import load as image_load

class AssetsLoader:
    def __init__(self) -> None:
        pass

    def load(self, dir_path: str) -> dict:
        if '.png' in dir_path:
            return image_load(dir_path)
        return {path.split('.')[0] : self.load(dir_path + '/' + path) for path in listdir(dir_path)}
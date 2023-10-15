from os import listdir
from pygame.image import load as image_load

class AssetsLoader:
    def __init__(self) -> None:
        pass

    def load(self, dir_path: str, type: str) -> dict:
        '''Recursive load directory with assets

        Example type: '.png'
        '''

        if type in dir_path:
            return image_load(dir_path)
        return {path.split('.')[0] : self.load(dir_path + '/' + path, type) for path in listdir(dir_path)}
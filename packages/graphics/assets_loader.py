from os import listdir, name as os_name
from pygame.image import load as image_load
from pygame import Surface, Rect
from pygame.transform import flip, scale
from .const import SPRITE_SIZE, ANIMATION_LEN, ANIMATION_NAMES, ANIMATION_DIRECTIONS, TILE_SIZE

class AssetsLoader:
    def __init__(self) -> None:
        pass

    def load(self, dir_path: str, type: str) -> dict:
        '''Recursive load directory with assets

        Example type: '.png'
        '''

        if type in dir_path:
            image = image_load(dir_path)
            if 'soldiers' in dir_path:
                return self.__cut_spritesheet(image)
            return scale(image, (TILE_SIZE, TILE_SIZE))
        
        if os_name == 'posix':
            if "./packages/graphics" not in dir_path:
                dir_path = "./packages/graphics" + dir_path


        path = {path.split('.')[0] : self.load(dir_path + '/' + path, type) for path in listdir(dir_path)}
        
        return path
    
    def __cut_spritesheet(self, sheet: Surface) -> dict[str:dict[str:dict[str:Surface]]]:
        size_x, size_y = sheet.get_size()

        all_textures = {}

        textures = [
            sheet.subsurface(Rect(x * SPRITE_SIZE, 0, 32, 32))
            for x in range(size_x // SPRITE_SIZE)
        ]

        for animation_number, name in enumerate(ANIMATION_NAMES):
            animation_textures = {}
            for direction_number, direction in enumerate(ANIMATION_DIRECTIONS):
                direction_textures = []
                for frame in range(ANIMATION_LEN):
                    direction_textures.append(textures[animation_number * ANIMATION_LEN * len(ANIMATION_DIRECTIONS) + direction_number * ANIMATION_LEN + frame])
                animation_textures[direction] = direction_textures
                if direction == 'right':
                    animation_textures['left'] = list(map(
                        lambda texture: flip(texture, True, False),
                        direction_textures
                    ))
            all_textures[name] = animation_textures

        return all_textures
    
    
        

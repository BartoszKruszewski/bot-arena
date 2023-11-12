from os import listdir, name as os_name
from pygame.image import load as image_load
from pygame import Surface, Rect, Color
from pygame.transform import flip
from .const import SPRITE_SIZE, ANIMATION_LEN, ANIMATION_NAMES, ANIMATION_DIRECTIONS, TILE_SIZE
from random import choice

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
            elif 'grass' in dir_path:
                return self.__randomize_grass(image)
            return image
        
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
    
    def __randomize_grass(self, texture: Surface) -> Surface:
        '''Radomize grass texture color
        '''
        return self.__randomize_color(
            texture, Color(160, 177, 89),
            [
                Color(160, 177, 89),
                Color(158, 178, 91),
                Color(156, 172, 93),
                Color(164, 181, 86)
            ])

    def __randomize_color(self, texture: Surface, key: Color, colors: list[Color]) -> Surface:
        '''Change key color of texture to random colors from list
        '''
        
        new_texture = Surface(texture.get_size())
        [
            new_texture.set_at((x, y), choice(colors))
            for x in TILE_SIZE for y in TILE_SIZE
            if texture.get_at((x, y)) == key
        ]
        return new_texture
        

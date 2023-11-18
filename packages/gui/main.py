from .game_render.game_render_main import Main as GameRender
from .map_generate.map_generate_main import Main as MapGenerate
from pygame import init

from time import sleep

class Main():
    def __init__(self, log_name: str):
        init()
        while True:
            # GameRender('example_log.txt')
            # sleep(1)
            MapGenerate()
            sleep(1)


        

        

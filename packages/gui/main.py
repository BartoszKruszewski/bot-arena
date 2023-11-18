from .game_render.game_render_main import Main as GameRender

class Main():
    def __init__(self, log_name: str):
        self.__game_render = GameRender(log_name)
        

        

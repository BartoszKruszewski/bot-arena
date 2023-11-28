from packages.gui.pygame_tree.gui_object import Scene, Window, GUIElement
from packages.gui.pygame_tree.buttons.radio_button import RadioButton
from .game_render.game_renderer import GameRender

def load_scene():
    return Scene([
            Window(
                [], 
                (0, 0), (0.2, 1),
                color=(42, 42, 42)),
            Window(
                [ 
                    GameRender((0, 0), (1, 1))
                ], 
                (0.2, 0), (0.8, 0.8),
                color=(84, 84, 84)
            ),
            Window(
                [
                ], 
                (0.2, 0.8), (1, 0.2),
                color=(126, 126, 126)),
        ], (0, 0), (1, 1))
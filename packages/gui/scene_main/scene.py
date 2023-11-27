from packages.gui.pygame_tree.gui_object import Scene, Window, GUIElement
from packages.gui.pygame_tree.buttons.button import Button

def load_scene(scene1_function, scene2_function, scene3_function):
    return Scene(
                [
                    Button(
                        (0.3, 0.4), (0.4, 0.1),
                        color=(255, 255, 0),
                        on_click=scene1_function
                    ),
                    Button(
                        (0.3, 0.6), (0.4, 0.1),
                        color=(0, 0, 255),
                        on_click=scene2_function
                    ),
                    Button(
                        (0.3, 0.8), (0.4, 0.1),
                        color=(255, 0, 0),
                        on_click=scene3_function
                    )  
                ],
            (0, 0), (1, 1),
        )
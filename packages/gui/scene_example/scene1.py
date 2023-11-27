from packages.gui.pygame_tree.gui_object import Scene, Window, GUIElement
from packages.gui.pygame_tree.buttons.radio_button import RadioButton

def load_scene():
    return Scene(
            [
                Window(
                [
                    # GUIElement(
                    #     (0.7, 0.5), (0.1, 0.1),
                    #     color=(255, 255, 0)
                    # ),
                    RadioButton(
                        (0.5, 0.5), (0.1, 0.1),
                        color=(255, 0, 0),
                        active_color=(0, 255, 0),
                        on_click=lambda: print('radio button clicked')
                    ),
                    RadioButton(
                        (0.6, 0.6), (0.1, 0.1),
                        color=(255, 0, 0),
                        active_color=(0, 255, 0),
                        on_click=lambda: print('radio button clicked')
                    )
                ],
                (0.5, 0), (0.5, 1)),
                Window(
                [
                    GUIElement(
                        (0, 0), (1, 1),
                        color=(0, 0, 255)
                    ),
                ],
                (0, 0), (0.5, 1)),
            ],
            (0, 0), (1, 1),
            )
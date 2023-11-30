from ..abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Scene, Window, RadioButton, NumberField, List, Grid

class ExampleSceneManager(AbstractSceneManager):
    def load_scene(self, scene_functions):
        return Scene([
            Window([
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
                ),
                NumberField((0.6, 0.6), (0.3, 0.1))
            ], (0.5, 0), (0.5, 1)),
            Window([
                Grid(
                    [[str(i*100 + j) for j in range(5)] for i in range(5)],
                    (0, 0), (0.5, 0.5),
                    color = (255, 0, 0),
                    on_click = lambda x,y: print(x, y)
                )
            ], (0, 0), (0.5, 1))
        ])
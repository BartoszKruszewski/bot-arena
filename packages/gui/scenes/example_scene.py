from ..abstract_scene_manager import AbstractSceneManager
from packages.gui.gui_objects import Scene, Window, RadioButton, NumberField, List, Grid, Slider

class ExampleSceneManager(AbstractSceneManager):
    def __init__(self, scene_functions=...):
        super().__init__(scene_functions)
        self.podswietleni = []

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
                    on_click = self.handle_soldier_click
                ),
                Slider((0.1, 0.7), (0.8, 0.1), color=(0, 255, 0), on_change=lambda x: print(x))
            ], (0, 0), (0.5, 1))
        ])
    
    def handle_soldier_click(self, x, y):
        if (x, y) not in self.podswietleni:
            self.podswietleni.append((x,y))
        else:
            self.podswietleni.remove((x,y))
        print(self.podswietleni)

    def handle_tower_click(self, x, y):
        pass

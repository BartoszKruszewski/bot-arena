from packages.gui.gui_objects.gui_object import GUIobject
from packages.gui.gui_objects.window import Window

class StatsDisplay(Window):
    def __init__(self, sub_objects: list[GUIobject], pos: tuple[float, float], size: tuple[float, float], update_dict, **kwargs):
        super().__init__(sub_objects, pos, size, **kwargs)

        self.update_dict = update_dict

    def update(self, dt) -> None:
        stats = self.update_dict()
        if stats:
            for stat in stats:
                for side in stats[stat]:
                    self.send_info(f'{side}_{stat}', "text", str(stats[stat][side]))
        super().update(dt)
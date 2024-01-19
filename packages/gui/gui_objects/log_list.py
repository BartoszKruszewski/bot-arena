from pygame import Surface
from pygame.event import Event
from packages.gui.gui_objects.list import List
from packages.file_manager import FileManager
from packages.gui.const import GUI_COLORS, FRAMERATE, MAX_HOVER_TIME
from packages import LOGS_DIRECTORY
from os import listdir, path

def ease(x):
    return 1 - (1 - x) * (1 - x)

class LogList(List):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], log_name: str, get_game_speed, **kwargs):
        file_name = path.join(LOGS_DIRECTORY, log_name)    

        manager = FileManager("LOGS")
        # log = manager.read_file(f'{log_name}/{file_name}').splitlines()[1:]
        log = manager.read_file(path.join(LOGS_DIRECTORY, file_name)).splitlines()[1:]
        super().__init__(log, pos, size, **kwargs)
        self.properties["log"] = log
        self.get_game_speed = get_game_speed
        self.step_size = (self.properties.get('button_size', (0.9, 0.1))[1] + self.properties.get('gap', (0.05, 0.01))[1])
        for object in self.sub_objects:
            object.pos[1] += self.step_size

    def handle_event(self, event: Event) -> None:
        pass

    def update(self, dt):
        super().update(dt)
        speed = self.get_game_speed()
        for i, object in enumerate(self.sub_objects):
            object.hover_time = (1 - abs(object.pos[1]) / self.step_size) * MAX_HOVER_TIME
            object.pos[1] -= speed * dt / FRAMERATE * self.step_size
        self.calc_pos()
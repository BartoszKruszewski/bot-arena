from pygame import Surface
from pygame.event import Event
from packages.gui.gui_objects.list import List
from packages.file_manager import FileManager
from packages.gui.const import GUI_COLORS
from packages import LOGS_DIRECTORY
from os import listdir

class LogList(List):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], log_name: str, get_log_index, **kwargs):
        file_name = listdir(f'{LOGS_DIRECTORY}/{log_name}')[-1]
        manager = FileManager("LOGS")
        log = manager.read_file(f'{log_name}/{file_name}').splitlines()[1:]
        super().__init__(log, pos, size, **kwargs)

        self.properties["log"] = log
        self.properties["log_length"] = len(log)
        self.properties["index"] = 0
        self.get_index = get_log_index
        self.ended = False

    def handle_event(self, event: Event) -> None:
        pass

    def update(self, dt):
        if self.properties["log_length"] - self.properties["index"] <= 9:
            self.ended = True

        index = self.properties["index"]
        if not self.ended:
            self.properties["index"] = self.get_index()
            
        if self.properties["index"] != index and not self.ended:
            self.sub_objects[self.properties["index"]].properties["active"] = True
            move = (self.properties.get('button_size', (0.9, 0.1))[1] + self.properties.get('gap', (0.05, 0.01))[1])
            for object in self.sub_objects:
                object.pos[1] = object.pos[1] - move
            self.calc_pos()

    def render(self) -> Surface:
        surf = Surface(self.real_size)
        surf.fill(self.properties.get('background_color', GUI_COLORS['background1']))
        for object in self.sub_objects[self.properties["index"] : self.properties["index"] + 9]:
            surf.blit(object.render(), object.real_pos)

        return surf
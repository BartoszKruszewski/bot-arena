from pygame import Vector2
from .object_rt import ObjectRT

class ObjectTracker:
    def __init__(self):
        self.objects_rt = {'left': {}, 'right': {}}

    def update(self, logic_objects, dt: float, mouse_pos: Vector2):
        self.__add_new_objects(logic_objects)
        self.__remove_dead_objects(logic_objects)
        self.__update_objects_stats(logic_objects)
        for object in self.get_objects():
            object.update(dt, mouse_pos)

    def __add_new_objects(self, logic_objects: dict[str, dict]):
        for side in ('left', 'right'):
            for logic_object in logic_objects[side]:
                id = logic_object.id
                if id not in self.objects_rt[side]:
                    self.objects_rt[side][id] = self.get_new_object(logic_object, side)

    def __remove_dead_objects(self, logic_objects: dict):
        ids_to_remove = {'left': [], 'right': []}
        for side in ('left', 'right'):
            for id in self.objects_rt[side]:
                if id not in [lo.id for lo in logic_objects[side]]:
                    ids_to_remove[side].append(id)
        
        for side in ('left', 'right'):
            for id in ids_to_remove[side]:
                self.objects_rt[side].pop(id)

    def __update_objects_stats(self, logic_objects):
        for side in ('left', 'right'):
            for logic_object in logic_objects[side]:
                id = logic_object.id
                self.objects_rt[side][id].set_stats(logic_object.__dict__())

    def get_new_object(self, logic_object, side: str) -> ObjectRT:
        pass

    def get_objects(self):
        return list(self.objects_rt['left'].values()) \
            + list(self.objects_rt['right'].values())

    def __str__(self):
        return f'[{", ".join(str(object) for object in self.get_objects())}]'
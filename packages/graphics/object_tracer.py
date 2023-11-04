from .soldier_animated_object import SoldierAnimatedObject
from ..game_logic.objects.soldiers import _Soldier

class ObjectTracer:
    def __init__(self):
        pass

    def update_soldier_animated_objects(self, soldiers: dict[str, list[_Soldier]], soldier_animated_objects: list[SoldierAnimatedObject]):
        positions = {}
        for side in soldiers:
            side_positions = {}
            for soldier in soldiers[side]:
                side_positions[soldier.id] = soldier.position
            positions[side] = side_positions

        soldier_animated_objects_ids = []
        for soldier_animated_object in soldier_animated_objects:
            if soldier_animated_object.id in positions['left']:
                soldier_animated_object.set_path_position(positions['left'][soldier_animated_object.id])
                soldier_animated_objects_ids.append(soldier_animated_object.id)
            elif soldier_animated_object.id in positions['right']:
                soldier_animated_object.set_path_position(positions['right'][soldier_animated_object.id])
                soldier_animated_objects_ids.append(soldier_animated_object.id)
            else:
                soldier_animated_objects.remove(soldier_animated_object)

        for side in positions:
            for id in positions[side]:
                if id not in soldier_animated_objects_ids:
                    soldier_animated_objects.append(SoldierAnimatedObject(positions[side][id], 'swordsman', side))

        
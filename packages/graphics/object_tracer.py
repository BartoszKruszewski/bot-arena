from .soldier_animated_object import SoldierAnimatedObject
from ..game_logic.objects.soldiers import _Soldier
from pygame import Vector2
from .const import TILE_SIZE

class ObjectTracer:
    def __init__(self, path):
        self.__spawn_pos = {
            'left': Vector2(path[0]),
            'right': Vector2(path[-1])
        } 

    def update_soldier_animated_objects(self, soldiers: dict[str, list[_Soldier]], soldier_animated_objects: list[SoldierAnimatedObject]):
        soldiers_data = {}
        for side in ('left', 'right'):
            side_data = {}
            for soldier in soldiers[side]:
                side_data[soldier.id] = soldier
            soldiers_data[side] = side_data

        sao_data = {}
        for side in ('left', 'right'):
            side_data = {}
            for sao in soldier_animated_objects:
                if side == sao.side:
                    side_data[sao.id] = sao
            sao_data[side] = side_data

        for side in ('left', 'right'):
            for soldier_id in soldiers_data[side]:
                soldier_data = soldiers_data[side][soldier_id]
                if soldier_id in sao_data[side]:
                    print(soldier_data.hp)
                    sao_data[side][soldier_id].set_path_position(soldier_data.position)
                    sao_data[side][soldier_id].set_animation('walk' if soldier_data.can_move else 'fight')
                else:
                    soldier_animated_objects.append(SoldierAnimatedObject(
                        soldier_data.position,
                        self.__spawn_pos[side] * TILE_SIZE,
                        'swordsman',
                        side
                    ))
        
        for side in ('left', 'right'):
            for sao_id in sao_data[side]:
                if sao_id not in soldiers_data[side]:
                    soldier_animated_objects.remove(sao_data[side][sao_id]) 
        
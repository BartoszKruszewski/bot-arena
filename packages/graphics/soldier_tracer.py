from .soldier_rt import SoldierRT
from ..game_logic.objects.soldiers import _Soldier

class SoldierTracer:
    def __init__(self, path: list[tuple[int, int]]):
        self.__path = path
        SoldierRT.path = path
        self.__fight_pos = None
        self.soldiers_rt = []

    def update(self, soldiers: dict[str, list[_Soldier]]):
        soldiers_data = {}
        for side in ('left', 'right'):
            side_data = {}
            for soldier in soldiers[side]:
                side_data[soldier.id] = soldier
            soldiers_data[side] = side_data

        srt_data = {}
        for side in ('left', 'right'):
            side_data = {}
            for srt in self.soldiers_rt:
                if side == srt.side:
                    side_data[srt.id] = srt
            srt_data[side] = side_data

        is_fight_pos_set = False
        for id_left in soldiers_data['left']:
            for id_right in soldiers_data['right']:
                if soldiers_data['left'][id_left].position == soldiers_data['right'][id_right].position:
                    is_fight_pos_set = True
                    self.__fight_pos = soldiers_data['left'][id_left].position
        if not is_fight_pos_set:
            self.__fight_pos = None


        for side in ('left', 'right'):
            for soldier_id in soldiers_data[side]:
                soldier_data = soldiers_data[side][soldier_id]
                if soldier_id in srt_data[side]:
                    srt_data[side][soldier_id].set_path_position(soldier_data.position)
                    if soldier_data.position == self.__fight_pos:
                        state = 'fight'
                    elif self.__fight_pos is not None and abs(soldier_data.position - self.__fight_pos) == 1:
                        state = 'idle'
                    else:
                        state = 'walk'
                        
                    srt_data[side][soldier_id].set_state(state)
                else:
                    self.soldiers_rt.append(SoldierRT(
                        soldier_data.id,
                        soldier_data.position,
                        'swordsman',
                        side
                    ))
        
        for side in ('left', 'right'):
            for srt_id in srt_data[side]:
                if srt_id not in soldiers_data[side]:
                    self.soldiers_rt.remove(srt_data[side][srt_id])

        self.__update_soldiers_rt()

    def __update_soldiers_rt(self):
        for soldier in self.soldiers_rt:
            soldier.update()

    def get_soldiers(self):
        return self.soldiers_rt
    
        
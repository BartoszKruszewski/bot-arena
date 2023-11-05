from .soldier_rt import SoldierRT
from ..game_logic.objects.soldiers import _Soldier

class SoldierTracer:
    def __init__(self, path: list[tuple[int, int]]):
        SoldierRT.path = path
        self.__fight_pos = None
        self.soldiers_rt = {'left': {}, 'right': {}}

    def __parse_soldiers_data(self, soldiers: dict[str, list[_Soldier]]):
        soldiers_data = {}
        for side in ('left', 'right'):
            side_data = {}
            for soldier in soldiers[side]:
                side_data[soldier.id] = soldier
            soldiers_data[side] = side_data

        return soldiers_data

    def __update_fight_pos(self, soldiers_data: dict[int, list[_Soldier]]):
        is_fight_pos_set = False
        for id_left in soldiers_data['left']:
            for id_right in soldiers_data['right']:
                if soldiers_data['left'][id_left].position == \
                    soldiers_data['right'][id_right].position:
                    is_fight_pos_set = True
                    self.__fight_pos = soldiers_data['left'][id_left].position
        if not is_fight_pos_set:
            self.__fight_pos = None

    def update(self, soldiers: dict[str, list[_Soldier]]):
        
        soldiers_data = self.__parse_soldiers_data(soldiers)
        self.__update_fight_pos(soldiers_data)

        for side in ('left', 'right'):
            for id in soldiers_data[side]:
                soldier_data = soldiers_data[side][id]
                if id in self.soldiers_rt[side]:
                    self.soldiers_rt[side][id].set_path_position(soldier_data.position)
                    if soldier_data.position == self.__fight_pos:
                        state = 'fight'
                    elif self.__fight_pos is not None and \
                        abs(soldier_data.position - self.__fight_pos) == 1:
                        state = 'idle'
                    else:
                        state = 'walk'
                    self.soldiers_rt[side][id].set_state(state)
                else:
                    self.soldiers_rt[side][id] = SoldierRT(
                        soldier_data.id,
                        soldier_data.position,
                        'swordsman',
                        side
                    )

        soldier_ids_to_remove = {'left': [], 'right': []}
        for side in ('left', 'right'):
            for id in self.soldiers_rt[side]:
                if id not in soldiers_data[side]:
                    soldier_ids_to_remove[side].append(id)

        for side in ('left', 'right'):
            for id in soldier_ids_to_remove[side]:
                self.soldiers_rt[side].pop(id)

        self.__update_soldiers_rt()

    def get_soldiers(self):
        return list(self.soldiers_rt['left'].values()) + \
              list(self.soldiers_rt['right'].values())
    
    def __update_soldiers_rt(self):
        for soldier in self.get_soldiers():
            soldier.update()
    
        
from .soldier_rt import SoldierRT
from ..game_logic.objects.soldiers import _Soldier

class SoldierTracker:
    '''Soldier objects tracker.

    Track Soldier objects from game logic and
    synchronize them with real time soldier
    objects in the graphics module. 
    '''

    def __init__(self, path: list[tuple[int, int]]):
        SoldierRT.path = path
        self.soldiers_rt = {'left': {}, 'right': {}}

    def __parse_soldiers_data(self, soldiers: dict[str, list[_Soldier]]) -> dict[str, dict[int, _Soldier]]:
        '''Parsing soldier data.

        From:
            {
                'left':  [Soldier, ...],
                'right': [Soldier, ...]
            }

        To:
            {
                'left': {
                    id0: Soldier,
                    id1: Soldier,
                    ...
                },
                'right': {
                    id0: Soldier,
                    id1: Soldier,
                    ...
                }
            }
        '''

        soldiers_data = {}
        for side in ('left', 'right'):
            side_data = {}
            for soldier in soldiers[side]:
                side_data[soldier.id] = soldier
            soldiers_data[side] = side_data

        return soldiers_data

    def __get_fight_pos(self, soldiers: dict[str, list[_Soldier]]) -> dict[str, int]:
        '''Returns soldiers fight path pos.

        Position of two enemy soldiers in the neightbouring path pos.
        It can be only one that situation at one time.
        '''

        left_positions = [s.position for s in soldiers['left']]
        right_positions = [s.position for s in soldiers['right']]
        for l_pos in left_positions:
            for r_pos in right_positions:
                if abs(l_pos - r_pos) <= 1:
                    return {'left': l_pos, 'right': r_pos}
        return {'left': -1, 'right': -1}

    def update_tracker(self, soldiers: dict[str, list[_Soldier]]) -> None:
        '''Update number and state of real time soldiers,
        based on soldiers from game logic.

        Impact on graphics state:
            - adding new real time soldiers
            - removing soldiers that should be dead
            - updating path position of real time soldiers
            - updating state of real time soldiers
        '''
        
        soldiers_data = self.__parse_soldiers_data(soldiers)
        fight_pos = self.__get_fight_pos(soldiers)

        sorted_soldiers = {
            'left': sorted(soldiers['left'], key = lambda s: s.position, reverse=True),
            'right': sorted(soldiers['right'], key = lambda s: s.position)
        }

        for side in ('left', 'right'):
            for id in soldiers_data[side]:
                soldier_data = soldiers_data[side][id]
                if id in self.soldiers_rt[side]:
                    self.soldiers_rt[side][id].set_path_position(soldier_data.position)

                    if fight_pos[side] == -1:
                        state = 'walk'
                    else:
                        if sorted_soldiers[side].index(soldier_data) == 0:
                            state = 'fight'
                        elif abs(soldier_data.position - fight_pos[side]) <= sorted_soldiers[side].index(soldier_data):
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

    def update_soldiers(self) -> None:
        '''Updates every real time soldier.
        '''

        for soldier in self.get_soldiers():
            soldier.update()

    def get_soldiers(self) -> list[SoldierRT]:
        '''Real time soldiers getter.
        '''

        return list(self.soldiers_rt['left'].values()) + \
              list(self.soldiers_rt['right'].values())
    
    def __str__(self):
        return f'[{", ".join(str(soldier) for soldier in self.get_soldiers())}]'


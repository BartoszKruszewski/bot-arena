from .stats import COST
from .map import Map
from .actions import Action 
from . import actions

class Game:
    def __init__(self):
        self._map = Map()
        self._time = 0

    def get_map(self) -> Map:
        return self._map

    def __make_action(self, action : Action) -> None:
        pass

    def __action_handler(self, action_left : Action, action_right : Action) -> None:
        if isinstance(action_left, actions.BuildTurret) and isinstance(action_right, actions.BuildTurret):
            if action_left.cord == action_right.cord:
                return "Both players can't build turret in the same place"
            
        self.__make_action(action_left)
        self.__make_action(action_right)


    def __update_soldiers(self) -> None:
        left_soldiers = self._map.soliders['left']
        right_soldiers = self._map.soliders['right']
    
        def attack_phase() -> tuple[int, int]:
            for i in range(len(self._map.path) - 1):
                if left_soldiers[i] and right_soldiers[i]:
                    left_soldiers[i] -= 10
                    right_soldiers[i] -= 10

                    if left_soldiers[i] <= 0: left_soldiers[i] = None
                    if right_soldiers[i] <= 0: right_soldiers[i] = None

                    return (i, i)
                
                if left_soldiers[i] and right_soldiers[i + 1]:   
                    left_soldiers[i] -= 10
                    right_soldiers[i + 1] -= 10

                    if left_soldiers[i] <= 0: left_soldiers[i] = None
                    if right_soldiers[i + 1] <= 0: right_soldiers[i + 1] = None

                    return (i, i + 1)
                
            return (-999, -999)
        
        def move_phase(where_attack) -> None:
            new_left_soldiers = {i: None for i in range(len(self._map.path))}
            new_right_soldiers = {i: None for i in range(len(self._map.path))}

            for i in range(1, len(self._map.path)):
                if i == where_attack[1]:
                    new_right_soldiers[i] = right_soldiers[i]
                    continue
                if new_right_soldiers[i-1] is None:
                    new_right_soldiers[i-1] = right_soldiers[i]

            for i in range(len(self._map.path) - 2, -1, -1):
                if i == where_attack[0]:
                    new_left_soldiers[i] = left_soldiers[i]
                    continue
                if new_left_soldiers[i+1] is None:
                    new_left_soldiers[i+1] = left_soldiers[i]

            self._map.soliders['left'] = new_left_soldiers
            self._map.soliders['right'] = new_right_soldiers

        where_attack = attack_phase()
        move_phase(where_attack)

    def __update_map(self) -> None:
        self.__update_soldiers()
        # turrets attack
        # resources

    def update(self, action_left : Action, action_right : Action) -> None:
        self.__update_map()
        # make players actions
        self._time += 1


    

from .stats import COST
from .map import Map
from .actions import Action 
from . import actions

ErrorCode = {
    -2: "Win",
    -1: "Lose",
    0: "OK",
    1: "Both players can't build turret in the same place",
    2: "Not enough gold",
    3: "Can't build turret on path or obstacle",
    4: "Too many soldiers on the path"
}

class Game:
    def __init__(self):
        self._map = Map()
    
    def __update_resources(self) -> None:
        self._map.stats['left']['gold'] += 100
        self._map.stats['right']['gold'] += 100

    def __update_soldiers(self) -> None:
        left_soldiers = self._map.soldiers['left']
        right_soldiers = self._map.soldiers['right']
    
        def attack_phase() -> tuple[int, int]:
            for i in range(len(self._map.path) - 1):
                if left_soldiers[i] and right_soldiers[i]:
                    left_soldiers[i] -= 1 # attack -1 hp
                    right_soldiers[i] -= 1 # attack -1 hp

                    if left_soldiers[i] <= 0: left_soldiers[i] = None
                    if right_soldiers[i] <= 0: right_soldiers[i] = None

                    return (i, i)
            for i in range(len(self._map.path) - 1):
                if left_soldiers[i] and right_soldiers[i + 1]:   
                    left_soldiers[i] -= 1 # attack -1 hp
                    right_soldiers[i + 1] -= 1 # attack -1 hp

                    if left_soldiers[i] <= 0: left_soldiers[i] = None
                    if right_soldiers[i + 1] <= 0: right_soldiers[i + 1] = None

                    return (i, i + 1)
                
            return (-999, -999)
        
        def move_phase(where_attack) -> None:
            new_left_soldiers = {i: None for i in range(-1, len(self._map.path)+2)}
            new_right_soldiers = {i: None for i in range(-1, len(self._map.path)+2)}

            for i in range(0, len(self._map.path)):
                if i == where_attack[1]:
                    new_right_soldiers[i] = right_soldiers[i]
                    continue
                if new_right_soldiers[i-1] is None:
                    new_right_soldiers[i-1] = right_soldiers[i]
                else:
                    new_right_soldiers[i] = right_soldiers[i]

            for i in range(len(self._map.path) - 1, -1, -1):
                if i == where_attack[0]:
                    new_left_soldiers[i] = left_soldiers[i]
                    continue
                if new_left_soldiers[i+1] is None:
                    new_left_soldiers[i+1] = left_soldiers[i]
                else:
                    new_left_soldiers[i] = left_soldiers[i]

            self._map.soldiers['left'] = new_left_soldiers
            self._map.soldiers['right'] = new_right_soldiers

        where_attack = attack_phase()
        move_phase(where_attack)

    def __update_turrets_attacks(self) -> None:
        def manhattan_distance(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        left_turrets = self._map.structures['left']['turret']
        right_turrets = self._map.structures['right']['turret']

        left_soldiers_ids = [i for i in range(len(self._map.path)) if self._map.soldiers['left'][i] is not None]
        right_soldiers_ids = [i for i in range(len(self._map.path)) if self._map.soldiers['right'][i] is not None]

        for left_soldier_id in left_soldiers_ids:
            left_soldier_cords = self._map.path[left_soldier_id]
            for right_turret_cord in right_turrets:
                if manhattan_distance(left_soldier_cords, right_turret_cord) <= 3:
                    self._map.soldiers['left'][left_soldier_id] -= 1
                    if self._map.soldiers['left'][left_soldier_id] <= 0:
                        self._map.soldiers['left'][left_soldier_id] = None
                    break

        for right_soldier_id in right_soldiers_ids:
            right_soldier_cords = self._map.path[right_soldier_id]
            for left_turret_cord in left_turrets:
                if manhattan_distance(right_soldier_cords, left_turret_cord) <= 3:
                    self._map.soldiers['right'][right_soldier_id] -= 1
                    if self._map.soldiers['right'][right_soldier_id] <= 0:
                        self._map.soldiers['right'][right_soldier_id] = None
                    break

    def __update_map(self) -> None:
        self.__update_resources()
        self.__update_soldiers()
        self.__update_turrets_attacks()

    def __make_action(self, action : Action) -> ErrorCode:
        if isinstance(action, actions.BuildTurret):
            if self._map.stats[action.player]['gold'] < COST['turret']['gold']:
                return ErrorCode[2]
            
            if action.cord in self._map.structures['left']['turret'] or action.cord in self._map.structures['right']['turret']:
                if action.cord in self._map.path or action.cord in self._map.obstacles:
                    return ErrorCode[3]

            self._map.structures[action.player]['turret'].append(action.cord)
            self._map.stats[action.player]['gold'] -= COST['turret']['gold']
            return ErrorCode[0]
        
        if isinstance(action, actions.SpawnSoldier):
            if self._map.stats[action.player]['gold'] < COST['soldier']['gold']:
                return ErrorCode[2]
            if action.player == 'left':
                if self._map.soldiers['left'][0] is not None:
                    return ErrorCode[4]
                self._map.soldiers['left'][0] = 9 # set soldier hp
                return ErrorCode[0]
            
            if action.player == 'right':
                if self._map.soldiers['right'][len(self._map.path) - 1] is not None:
                    return ErrorCode[4]
                self._map.soldiers['right'][len(self._map.path) - 1] = 9 # set soldier hp
                return ErrorCode[0]
            
        return ErrorCode[0]
            
    def __action_handler(self, action_left : Action, action_right : Action) -> tuple[ErrorCode, ErrorCode]:
        if isinstance(action_left, actions.BuildTurret) and isinstance(action_right, actions.BuildTurret):
            if action_left.cord == action_right.cord:
                return (ErrorCode[1], ErrorCode[1])
        
        return (self.__make_action(action_left), self.__make_action(action_right))

    def __check_win(self) -> int:
        if self._map.soldiers['left'][len(self._map.path)] is not None:
            return (ErrorCode[-2], ErrorCode[-1])
        if self._map.soldiers['right'][-1] is not None:
            return (ErrorCode[-1], ErrorCode[-2])
        return (ErrorCode[0], ErrorCode[0])

    def update(self, action_left : Action, action_right : Action) -> tuple[ErrorCode, ErrorCode]:
        self.__update_map()

        response = self.__action_handler(action_left, action_right)
        is_win = self.__check_win()
        
        if is_win != (ErrorCode[0], ErrorCode[0]):
            return is_win
        
        return response
    
    def get_map(self) -> Map:
        return self._map

    def get_path(self) -> list[tuple[int, int]]:
        return self._map.path
    
    def get_obstacles(self) -> list[tuple[int, int]]:
        return self._map.obstacles
    
    def get_structures(self) -> dict[str, list[tuple[int, int]]]:
        return self._map.structures
    
    def get_soldiers(self) -> dict[str, dict[int, int]]:
        return self._map.soldiers
    
    def get_stats(self) -> dict[str, dict[str, int]]:
        return self._map.stats
    
    def get_map_size(self) -> tuple[int, int]:
        return (self._map.MAP_SIZE_X, self._map.MAP_SIZE_Y)


    

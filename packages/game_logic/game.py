from .stats import COST
from .stats import START_GOLD, PASSIVE_GOLD
from .stats import SOLDIERS_STATS

from .actions import Action, BuildAction
from .actions import Wait, BuildTurret, BuildFarm, SpawnSoldier

from .objects.map import Map
from .objects.turrets import Turrets, Turret
from .objects.soldiers import Soldiers, Soldier
from .objects.farms import Farms, Farm

from packages import MAPS_DIRECTORY

ErrorCode = {
    -5: 'Too many troops',
    -4: 'Wrong build place',
    -3: 'Same build place',
    -2: 'Wrong action',
    -1: 'Not enough gold',
    0: 'OK',
    1: 'Left win',
    2: 'Right win',
    3: 'Tie'
}

class Game:
    def __init__(self, map_path: str = MAPS_DIRECTORY + "/example_map.json") -> None:
        self._map = Map(map_path)

        self.turrets = {
            'left': Turrets(self._map.path),
            'right': Turrets(self._map.path)
        }

        self.soldiers  = {
            'left': Soldiers('left', self._map.path),
            'right': Soldiers('right', self._map.path)
        }

        self.farms = {
            'left': Farms(self._map.path),
            'right': Farms(self._map.path)
        }

        self.gold = {
            'left': START_GOLD,
            'right': START_GOLD
        }

        self.income = {
            'left': PASSIVE_GOLD,
            'right': PASSIVE_GOLD
        }

        self.action_left = Wait('left')
        self.action_right = Wait('right')

    def __update_soldiers(self) -> None:
        self.soldiers['left'].fight(self.soldiers['right'])
        self.soldiers['right'].fight(self.soldiers['left'])

        self.soldiers['left'].move()
        self.soldiers['right'].move()

    def __shoot_turrets(self) -> None:
        self.turrets['left'].shoot(self.soldiers['right'])
        self.turrets['right'].shoot(self.soldiers['left'])
        
    def __handle_actions_error(self) -> tuple[int, int]:
        def check_build_place(action: Action) -> int:
            if self.gold[action.side] < COST['turret']:
                return -1
            if action.cords[0] < 0 or action.cords[0] >= self._map.MAP_SIZE_X or action.cords[1] < 0 or action.cords[1] >= self._map.MAP_SIZE_Y:
                return -4
            
            wrong_build_places = [
                self._map.obstacles, 
                self._map.path, 
                self.turrets['left'], 
                self.turrets['right'], 
                self.farms['left'], 
                self.farms['right']
                ]

            for place in wrong_build_places:
                if action.cords in place:
                    return -4
                
            return 0
        
        def check_spawn_soldier(action: Action) -> int:
            soldier_name = action.name
            if self.gold[action.side] < SOLDIERS_STATS[soldier_name]['cost']:
                return -1
            if not self.soldiers[action.side].can_spawn():
                return -5
            return 0

        # if same build place
        if isinstance(self.action_left, BuildTurret) and isinstance(self.action_right, BuildTurret):
            if self.action_left.cords == self.action_right.cords:
                return (-3, -3)
            
        left_error = None
        right_error = None

        left_error = check_build_place(self.action_left) if isinstance(self.action_left, BuildAction) else 0
        right_error = check_build_place(self.action_right) if isinstance(self.action_right, BuildAction) else 0
        
        left_error = check_spawn_soldier(self.action_left) if isinstance(self.action_left, SpawnSoldier) else left_error
        right_error = check_spawn_soldier(self.action_right) if isinstance(self.action_right, SpawnSoldier) else right_error

        self.action_left = Wait('left') if left_error else self.action_left
        self.action_right = Wait('right') if right_error else self.action_right

        return (left_error, right_error)

    def __execute_actions(self) -> None:
        def build(action: Action) -> None:
            if isinstance(action, BuildTurret):
                self.gold[action.side] -= COST['turret']
                self.turrets[action.side].spawn(action.cords)
                return
            if isinstance(action, BuildFarm):
                self.gold[action.side] -= COST['farm']
                self.farms[action.side].spawn(action.cords)
                return
            
        def spawn(action: Action) -> None:
            soldier_name = action.name
            self.gold[action.side] -= SOLDIERS_STATS[soldier_name]['cost']
            self.soldiers[action.side].spawn(soldier_name)

        action_to_function = {
            BuildTurret: build,
            BuildFarm: build,
            SpawnSoldier: spawn,
            Wait: lambda action: None
        }

        action_to_function[self.action_left.__class__](self.action_left)
        action_to_function[self.action_right.__class__](self.action_right)

    def __is_win(self) -> tuple[bool, bool]:
        left_win = self.soldiers['left'].is_win
        right_win = self.soldiers['right'].is_win

        if left_win and right_win:
            return (ErrorCode[3], ErrorCode[3])
        if left_win:
            return (ErrorCode[1], ErrorCode[1])
        if right_win:
            return (ErrorCode[2], ErrorCode[2])
        
        return None

    def update(self, action_left: Action, action_right: Action) -> tuple[str, str]:
        self.income['left'] += len(self.farms['left']) * 2
        self.income['right'] += len(self.farms['right']) * 2

        self.__update_soldiers()
        self.__shoot_turrets()
        self.soldiers['left'].clear_dead()
        self.soldiers['right'].clear_dead()

        self.action_left = action_left
        self.action_right = action_right
        Error = self.__handle_actions_error()
        self.__execute_actions()
        
        self.gold['left'] += self.income['left']
        self.gold['right'] += self.income['right']

        WinLog = self.__is_win()
        if WinLog:
            self.update = lambda action_left, action_right: self.__is_win()
            return WinLog

        return (ErrorCode[Error[0]], ErrorCode[Error[1]])
    
    def get_path(self) -> list[tuple[int, int]]:
        return self._map.path
    
    def get_obstacles(self) -> list[tuple[int, int]]:
        return self._map.obstacles.obstacles
    
    def get_map_size(self) -> tuple[int, int]:
        return (self._map.MAP_SIZE_X, self._map.MAP_SIZE_Y)

    def get_soldiers(self) -> dict[str, list[Soldier]]:
        return {
            'left': self.soldiers['left'].soldiers,
            'right': self.soldiers['right'].soldiers
        }

    def get_turrets(self) -> dict[str, list[Turret]]:
        return {
            'left': self.turrets["left"].turrets,
            'right': self.turrets["right"].turrets
        }

    def get_farms(self) -> dict[str, list[Farm]]:
        return {
            'left': self.farms['left'].farms,
            'right': self.farms['right'].farms
        }

    def get_gold(self) -> dict[str, int]:
        return self.gold
    
    def get_income(self) -> dict[str, int]:
        return self.income

    def display(self) -> None:
        for turret in self.turrets['left'].turrets:
            print(turret.cords, end=' ')
        print()

        for i in range(self._map.MAP_SIZE_Y):
            for j in range(self._map.MAP_SIZE_X):
                try:
                    if (j, i) in self.soldiers['left']:
                        print('l', end='')
                    elif (j, i) in self.soldiers['right']:
                        print('r', end='')
                    elif (j, i) in self._map.path:
                        print('_', end='')
                    elif (j, i) in self.turrets['left']:
                        print('L', end='')
                    elif (j, i) in self.turrets['right']:
                        print('R', end='')
                    else:
                        print('.', end='')
                except:
                    if (j, i) in self._map.path:
                        print('O', end='')
                    else:
                        print('.', end='')

            print()
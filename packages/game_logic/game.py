from .stats import COST
from .stats import START_RESOURCES
from .objects.map import Map
from .actions import Action 
from . import actions
from .objects.turrets import Turrets
from .objects.soldiers import Soldiers

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
    def __init__(self):
        self._map = Map()

        self.turrets = {
            'left': Turrets(),
            'right': Turrets()
        }

        self.soldiers  = {
            'left': Soldiers('left', self._map.path),
            'right': Soldiers('right', self._map.path)
        }

        self.gold = {
            'left': START_RESOURCES['gold'],
            'right': START_RESOURCES['gold']
        }

        self.action_left = actions.Wait('left')
        self.action_right = actions.Wait('right')

    def _update_soldiers(self) -> None:
        self.soldiers['left'].fight(self.soldiers['right'])

        self.soldiers['left'].move()
        self.soldiers['right'].move()
        
    def _handle_actions_error(self) -> tuple[int, int]:
        def check_build_place(action: Action) -> int:
            if self.gold[action.side] < COST['turret']['gold']:
                return -1
            if action.cords < 0 or action.cords >= self._map.MAP_SIZE_X:
                return -4
            if action.cords in self._map.obstacles:
                return -4
            return 0
        
        def check_spawn_soldier(action: Action) -> int:
            if self.gold[action.side] < COST['soldier']['gold']:
                return -1
            if not self.soldiers[action.side].can_spawn():
                return -5
            return 0

        # if same build place
        if isinstance(self.action_left, actions.BuildTurret) and isinstance(self.action_right, actions.BuildTurret):
            if self.action_left.cords == self.action_right.cords:
                return (-3, -3)
            
        left_error = None
        right_error = None

        left_error = check_build_place(self.action_left) if isinstance(self.action_left, actions.BuildTurret) else 0
        right_error = check_build_place(self.action_right) if isinstance(self.action_right, actions.BuildTurret) else 0
        left_error = check_spawn_soldier(self.action_left) if isinstance(self.action_left, actions.SpawnSoldier) else left_error
        right_error = check_spawn_soldier(self.action_right) if isinstance(self.action_right, actions.SpawnSoldier) else right_error

        self.action_left = actions.Wait('left') if left_error else self.action_left
        self.action_right = actions.Wait('right') if right_error else self.action_right

        return (left_error, right_error)

    def _execute_actions(self) -> None:
        def build(action: Action) -> None:
            self.gold[action.side] -= COST['turret']['gold']
            self.turrets[action.side].spawn(action.cords)

        def spawn(action: Action) -> None:
            self.gold[action.side] -= COST['soldier']['gold']
            self.soldiers[action.side].spawn()

        action_to_function = {
            actions.BuildTurret: build,
            actions.SpawnSoldier: spawn,
            actions.Wait: lambda action: None
        }


        action_to_function[self.action_left.__class__](self.action_left)
        action_to_function[self.action_right.__class__](self.action_right)

    def is_win(self) -> tuple[bool, bool]:
        return (self.soldiers['left'].is_win(), self.soldiers['right'].is_win())


    def update(self, action_left: Action, action_right: Action) -> int:
        self._update_soldiers()

        self.action_left = action_left
        self.action_right = action_right
        Error = self._handle_actions_error()
        self._execute_actions()
        WinLog = self.is_win()

        if WinLog[0] and WinLog[1]: return (3, 3)
        if WinLog[0]: return (1, 1)
        if WinLog[1]: return (2, 2)
        return Error

    def display(self) -> None:
        import os
        # os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self._map.MAP_SIZE_Y):
            for j in range(self._map.MAP_SIZE_X):
                try:
                    if (j, i) in self.soldiers['left']:
                        print('l', end='')
                    elif (j, i) in self.soldiers['right']:
                        print('r', end='')
                    elif (j, i) in self._map.path:
                        print('O', end='')
                    else:
                        print('.', end='')
                except:
                    if (j, i) in self._map.path:
                        print('O', end='')
                    else:
                        print('.', end='')


            print()


    




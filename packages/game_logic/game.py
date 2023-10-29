from .stats import COST, START_RESOURCES
from .map import Map
from .actions import Action 
from . import actions

class Game:
    def __init__(self):
        self._map = Map()

        self._actions = []
        self._time = 0

    def get_map(self) -> Map:
        return self._map

    def __make_action(self, action : Action) -> None:
        pass

    def __action_handler(self, action_left : Action, action_right : Action) -> None:
        if isinstance(action_left, actions.BuildTurret) and isinstance(action_right, actions.BuildTurret):
            if action_left.cord == action_right.cord:
                return "Both players can't build turret in the same place"

        if isinstance(action_left, actions.SpawnSoldier):
            if self._map.soliders['left'][self.start] != []:
                return "Player left has too many soliders"
            
        if isinstance(action_right, actions.SpawnSoldier):
            if self._map.soliders['right'][self.start] != []:
                return "Player right has too many soliders"

    def update(self, action_left : Action, action_right : Action) -> None:
        self.__actions.append((action_left, action_right))
        self.__time += 1

        # calculate map
        # make players actions


    

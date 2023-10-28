from .stats import COST, START_RESOURCES
from .map import Map
from ..simulator.interpreter import Action

class Game:
    def __init__(self):
        self.__map = Map()

        self.stats = {side: {
                'gold': START_RESOURCES['gold'],
            } for side in ('left', 'right')
        }
        
        self.__map.generate_map()

    def get_map(self) -> Map:
        return self.__map

    def update(self):
        '''Main update function.

        Refereshes once per frame.
        '''

    def do_action(self, action: Action) -> bool:
        '''Performing actions
        '''

        # maping action -> its function
        ACTIONS = {
            'build': self.__a_build_structure,
        }

        # check is action name correct
        if action.name not in ACTIONS:
            return False

        # execute action function and get feedback
        return ACTIONS[action.name](action.value)

    def __a_build_structure(self, value: dict) -> bool:
        '''Build structure action function
        '''

        cord = value['cord']
        id = value['id']
        side = value['side']

        if self.__map.can_be_placed(cord, id):
            if self.__buy(id, side):
                self.__map.place_structure(cord, id)
                return True
        return False

    def __buy(self, id: str, side: str) -> bool:
        '''If it's possible buys a thing and gets feedback. 
        '''
        if self.__can_be_bought(id, side):
            self.stats[side]['gold'] -= COST[id]['gold']
            return True
        return False

    def __can_be_bought(self, id, side) -> bool:
        '''True if thing can be bought
        '''
        return COST[id]['gold'] <= self.stats[side]['gold']

    

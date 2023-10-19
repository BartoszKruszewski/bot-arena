from const import DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, CAMERA_OFFSET_MOVE_AREA, \
    CAMERA_OFFSET_SPEED, MAP_SIZE_PX_X, MAP_SIZE_PX_Y
from stats import COST, START_RESOURCES
from map import Map
from interpreter import Action
from mouse import Mouse
from pygame import Vector2

class Game:
    def __init__(self):
        self.map = Map()
        self.mouse = Mouse()

        self.camera_offset = Vector2(0, 0)
        self.__dest_camera_offset = Vector2(0, 0)
        self.__real_camera_offset = Vector2(0, 0)

        self.stats = {side: {
                'gold': START_RESOURCES['gold'],
                'food': START_RESOURCES['food'],
                'wood': START_RESOURCES['wood'],
                'base_hp': 10000,
            } for side in ('left', 'right')
        }
        
        self.map.generate_map()

    def update(self):
        '''Main update function.

        Refereshes once per frame.
        '''
        
        self.mouse.update()
        self.__update_camera_offset()

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

        if self.map.can_be_placed(cord, id):
            if self.__buy(id, side):
                self.map.place_structure(cord, id)
                return True
        return False

    def __buy(self, id: str, side: str) -> bool:
        '''If it's possible buys a thing and gets feedback. 
        '''
        if self.__can_be_bought(id, side):
            self.stats[side]['gold'] -= COST[id]['gold']
            self.stats[side]['wood'] -= COST[id]['wood']
            self.stats[side]['food'] -= COST[id]['food']
            return True
        return False

    def __can_be_bought(self, id, side) -> bool:
        '''True if thing can be bought
        '''
        return COST[id]['gold'] <= self.stats[side]['gold'] and \
            COST[id]['food'] <= self.stats[side]['food'] and \
            COST[id]['wood'] <= self.stats[side]['wood']

    def __update_camera_offset(self):
        
        if self.mouse.pos.x > DRAW_SCREEN_SIZE_X - CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.x -= CAMERA_OFFSET_SPEED
        elif self.mouse.pos.x < CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.x += CAMERA_OFFSET_SPEED

        if self.mouse.pos.y > DRAW_SCREEN_SIZE_Y - CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.y -= CAMERA_OFFSET_SPEED
        elif self.mouse.pos.y < CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.y += CAMERA_OFFSET_SPEED

        self.__dest_camera_offset.x = max(
            self.__dest_camera_offset.x, -(MAP_SIZE_PX_X - DRAW_SCREEN_SIZE_X))
        self.__dest_camera_offset.y = max(
            self.__dest_camera_offset.y, -(MAP_SIZE_PX_Y - DRAW_SCREEN_SIZE_Y))
        self.__dest_camera_offset.x = min(self.__dest_camera_offset.x, 0)
        self.__dest_camera_offset.y = min(self.__dest_camera_offset.y, 0)

        self.__real_camera_offset += (self.__dest_camera_offset - self.__real_camera_offset) / 20
        self.camera_offset = Vector2(
            int(self.__real_camera_offset.x), int(self.__real_camera_offset.y)) 

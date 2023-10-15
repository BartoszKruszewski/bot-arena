from const import DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, CAMERA_OFFSET_MOVE_AREA, \
    CAMERA_OFFSET_SPEED, MAP_SIZE_PX_X, MAP_SIZE_PX_Y
from map import Map
from interpreter import Action
from mouse import Mouse
from pygame import Vector2

class Game:
    def __init__(self):
        self.map = Map()
        self.camera_offset = Vector2(0, 0)
        self.mouse = Mouse()

    def update(self):
        self.mouse.update()
        self.update_camera_offset()

    def do_action(action: Action):
        ACTIONS = {}

        ACTIONS[action.name](action.value)

    def update_camera_offset(self):
        
        if self.mouse.pos.x > DRAW_SCREEN_SIZE_X - CAMERA_OFFSET_MOVE_AREA:
            self.camera_offset.x -= CAMERA_OFFSET_SPEED
        elif self.mouse.pos.x < CAMERA_OFFSET_MOVE_AREA:
            self.camera_offset.x += CAMERA_OFFSET_SPEED

        if self.mouse.pos.y > DRAW_SCREEN_SIZE_Y - CAMERA_OFFSET_MOVE_AREA:
            self.camera_offset.y -= CAMERA_OFFSET_SPEED
        elif self.mouse.pos.y < CAMERA_OFFSET_MOVE_AREA:
            self.camera_offset.y += CAMERA_OFFSET_SPEED

        self.camera_offset.x = max(self.camera_offset.x, -(MAP_SIZE_PX_X - DRAW_SCREEN_SIZE_X))
        self.camera_offset.y = max(self.camera_offset.y, -(MAP_SIZE_PX_Y - DRAW_SCREEN_SIZE_Y))
        self.camera_offset.x = min(self.camera_offset.x, 0)
        self.camera_offset.y = min(self.camera_offset.y, 0)


        

        

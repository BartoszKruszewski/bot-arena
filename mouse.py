from pygame.mouse import get_pos, get_pressed
from pygame import Vector2
from const import SCREEN_SIZE_X, DRAW_SCREEN_SIZE_X, SCREEN_SIZE_Y, DRAW_SCREEN_SIZE_Y

class Mouse:
    def __init__(self) -> None:
        self.pos = Vector2(0, 0)
        self.left_click = False
        self.right_click = False
        self.__left_switch = False
        self.__right_switch = False

    def update(self):
        '''Update mouse pos and buttons state.

        Buttons states are active for max one frame time. 
        '''

        x, y = get_pos()
        scale_x = DRAW_SCREEN_SIZE_X / SCREEN_SIZE_X
        scale_y = DRAW_SCREEN_SIZE_Y / SCREEN_SIZE_Y
        self.pos.x = x * scale_x
        self.pos.y = y * scale_y

        left, middle, right = get_pressed()

        if left:
            self.left_click = not self.__left_switch
            self.__left_switch = True
        else:
            self.__left_switch = False

        if right:
            self.right_click = not self.__right_switch
            self.__right_switch = True
        else:
            self.__right_switch = False
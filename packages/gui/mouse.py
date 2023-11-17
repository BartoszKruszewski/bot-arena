from pygame.mouse import get_pos, get_pressed
from pygame import Vector2, event, MOUSEWHEEL

class Mouse:
    def __init__(self) -> None:
        self.pos = Vector2(0, 0)
        self.left_click = False
        self.right_click = False
        self.wheel = 0
        self.__left_switch = False
        self.__right_switch = False

    def update(self):
        '''Update mouse pos and buttons state.

        Buttons states are active for max one frame time. 
        '''

        self.pos.x, self.pos.y = get_pos()
        left, middle, right = get_pressed()
        wheel_event = event.get(MOUSEWHEEL)
        self.wheel = wheel_event[0].y if wheel_event else 0

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
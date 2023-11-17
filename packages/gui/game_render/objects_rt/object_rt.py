from pygame import Vector2
from ...const import TILE_SIZE, FRAMERATE, ANIMATION_SPEED, \
    ANIMATION_LEN, MOUSE_TARGET_RADIUS, INFO_TAB_SHOW_SMOOTH, \
    INFO_TAB_SHOW_TIME, INFO_TAB_HIDE_SPEED

class ObjectRT():
    '''Real time object class used in game_render rendering.
    '''

    def __init__(self, cords: Vector2, id: int, name: str, side: str, stats: dict):

        # data
        self.cords = cords * TILE_SIZE
        self.id = id
        self.name = name
        self.side = side
        self.stats = stats

        # state
        self.frame = 0
        self.tick = 0
        self.state = 'idle'
        
        # info
        self.select_time = 0
        self.view_rate = [0] * (5 + len(self.stats))

    def update(self, dt: float, mouse_pos: Vector2): 
        '''Main update function.

        Refreshes once per frame.
        '''

        if self.state != 'idle':
            self.__update_frame(dt)

        self.__update_select_time(mouse_pos)

    def __update_frame(self, dt: float):
        '''Updates actual animation frame.
        '''

        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED * dt:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0

    def __update_select_time(self, mouse_pos: Vector2):
        if mouse_pos.distance_to(self.cords + Vector2(TILE_SIZE, TILE_SIZE) // 2) < MOUSE_TARGET_RADIUS:
            self.select_time += 1
            for i in range(5 + len(self.stats)):
                if i == 0 or self.view_rate[i - 1] > 0.9:
                    target = max(min(1, (self.select_time - i * INFO_TAB_SHOW_TIME // (5 + len(self.stats))) / INFO_TAB_SHOW_TIME), 0)
                else:
                    target = 0
                self.view_rate[i] += (target - self.view_rate[i]) / INFO_TAB_SHOW_SMOOTH
                if self.view_rate[i] < 0.1:
                    self.view_rate[i] = 0
        else:
            self.select_time = min(self.select_time, INFO_TAB_SHOW_TIME)
            self.select_time -= INFO_TAB_HIDE_SPEED
            self.select_time = max(self.select_time, 0)
            for i in range(5 + len(self.stats)):
                if i == 5 + len(self.stats) - 1 or self.view_rate[i + 1] == 0:
                    target = max(min(1, (self.select_time - i * INFO_TAB_SHOW_TIME // (5 + len(self.stats))) / INFO_TAB_SHOW_TIME), 0)
                else:
                    target = 1
                self.view_rate[i] += (target - self.view_rate[i]) / INFO_TAB_SHOW_SMOOTH * INFO_TAB_HIDE_SPEED
                if self.view_rate[i] < 0.1:
                    self.view_rate[i] = 0
         
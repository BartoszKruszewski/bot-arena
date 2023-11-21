from pygame import Vector2
from ...const import TILE_SIZE, FRAMERATE, ANIMATION_SPEED, \
    ANIMATION_LEN, MOUSE_TARGET_RADIUS, INFO_TAB_SHOW_SMOOTH, \
    INFO_TAB_SHOW_TIME, INFO_TAB_HIDE_SPEED

class ObjectRT:
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

    def update(self, dt: float, mouse_pos: Vector2): 
        '''Main update function.

        Refreshes once per frame.
        '''

        if self.state != 'idle':
            self.__update_frame(dt)

        self.__update_select_time(mouse_pos, dt)

    def set_stats(self, stats: dict):
        self.stats = stats

    def __getitem__(self, key):
        if key not in self.stats:
            raise Exception(f"Object doesn't have key stat: {key}")
        return self.stats[key]

    def __update_frame(self, dt: float):
        '''Updates actual animation frame.
        '''

        self.tick += 1
        if self.tick > FRAMERATE // ANIMATION_SPEED * dt:
            self.tick = 0
            self.frame += 1
            if self.frame >= ANIMATION_LEN:
                self.frame = 0

    def __update_select_time(self, mouse_pos: Vector2, dt: float):
        if mouse_pos.distance_to(self.cords + Vector2(TILE_SIZE, TILE_SIZE) // 2) < MOUSE_TARGET_RADIUS:
            self.select_time += dt
        else:
            self.select_time -= dt * INFO_TAB_HIDE_SPEED
        self.select_time = max(0, min(self.select_time, INFO_TAB_SHOW_TIME))

    def __str__(self):
        return f'<{self.side}:{self.id} {self.cords}>'
         
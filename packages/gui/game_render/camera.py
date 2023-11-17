from pygame import Vector2

from ..const import CAMERA_OFFSET_MOVE_AREA, CAMERA_OFFSET_SPEED, TILE_SIZE, \
    CAMERA_SMOOTH, FRAMERATE, STANDARD_FRAMERATE
from ..mouse import Mouse

class Camera:
    def __init__(self, map_size):
        self.__map_size = map_size
        self.__camera_offset = Vector2(0, 0)
        self.__dest_camera_offset = Vector2(0, 0)
        self.__real_camera_offset = Vector2(0, 0)
        self.__mouse_pos = Vector2(0, 0)
        

    def update(self, draw_screen_size: Vector2, mouse: Mouse, screen_shift: Vector2):
        self.__update_mouse_pos(mouse, screen_shift)
        self.__update_camera_offset(draw_screen_size)

    def get_offset(self) -> Vector2:
        return self.__camera_offset

    def get_mouse_pos(self) -> Vector2:
        return self.__mouse_pos - self.__camera_offset

    def __update_mouse_pos(self, mouse: Mouse, screen_shift: Vector2):
        self.__mouse_pos =  mouse.pos - screen_shift

    def __update_camera_offset(self, draw_screen_size: Vector2):
        
        camera_offset_move_area = draw_screen_size * CAMERA_OFFSET_MOVE_AREA

        if 0 <= self.__mouse_pos.x <= draw_screen_size.x and \
            0 <= self.__mouse_pos.y <= draw_screen_size.y:

            if self.__mouse_pos.x > draw_screen_size.x - camera_offset_move_area.x:
                self.__dest_camera_offset.x -= CAMERA_OFFSET_SPEED
            elif self.__mouse_pos.x < camera_offset_move_area.x:
                self.__dest_camera_offset.x += CAMERA_OFFSET_SPEED

            if self.__mouse_pos.y > draw_screen_size.y - camera_offset_move_area.x:
                self.__dest_camera_offset.y -= CAMERA_OFFSET_SPEED
            elif self.__mouse_pos.y < camera_offset_move_area.x:
                self.__dest_camera_offset.y += CAMERA_OFFSET_SPEED

            self.__dest_camera_offset.x = max(
                self.__dest_camera_offset.x, -(self.__map_size[0] * TILE_SIZE - draw_screen_size.x))
            self.__dest_camera_offset.y = max(
                self.__dest_camera_offset.y, -(self.__map_size[1] * TILE_SIZE - draw_screen_size.y))
            self.__dest_camera_offset.x = min(self.__dest_camera_offset.x, 0)
            self.__dest_camera_offset.y = min(self.__dest_camera_offset.y, 0)

        self.__real_camera_offset += (self.__dest_camera_offset - self.__real_camera_offset) \
                                        / CAMERA_SMOOTH / FRAMERATE * STANDARD_FRAMERATE
        self.__camera_offset = Vector2(
            int(self.__real_camera_offset.x), int(self.__real_camera_offset.y)) 
from pygame import Vector2

from ...const import CAMERA_OFFSET_MOVE_AREA, CAMERA_OFFSET_SPEED, TILE_SIZE, \
    CAMERA_SMOOTH
from ...mouse import Mouse

class Camera:
    def __init__(self, map_size):
        self.__map_size = map_size
        self.__camera_offset = Vector2(0, 0)
        self.__dest_camera_offset = Vector2(0, 0)
        self.__real_camera_offset = Vector2(0, 0)
        self.__mouse_pos = Vector2(0, 0)
        

    def update(self, draw_screen_size: Vector2, mouse: Mouse, screen_shift: Vector2, zoom: float, dt: float):
        self.__update_mouse_pos(mouse, screen_shift, zoom)
        self.__update_camera_offset(draw_screen_size, zoom, dt)

    def get_offset(self) -> Vector2:
        return self.__camera_offset

    def get_mouse_pos(self) -> Vector2:
        return self.__mouse_pos - self.__camera_offset

    def __update_mouse_pos(self, mouse: Mouse, screen_shift: Vector2, zoom: float):
        self.__mouse_pos =  (mouse.pos - screen_shift) / zoom

    def __update_camera_offset(self, draw_screen_size: Vector2, zoom: float, dt: float):
        
        camera_offset_move_area = draw_screen_size / zoom * CAMERA_OFFSET_MOVE_AREA

        if 0 <= self.__mouse_pos.x <= draw_screen_size.x / zoom and \
            0 <= self.__mouse_pos.y <= draw_screen_size.y / zoom:

            if self.__mouse_pos.x > draw_screen_size.x / zoom - camera_offset_move_area.x:
                self.__dest_camera_offset.x -= CAMERA_OFFSET_SPEED
            elif self.__mouse_pos.x < camera_offset_move_area.x:
                self.__dest_camera_offset.x += CAMERA_OFFSET_SPEED

            if self.__mouse_pos.y > draw_screen_size.y / zoom - camera_offset_move_area.x:
                self.__dest_camera_offset.y -= CAMERA_OFFSET_SPEED
            elif self.__mouse_pos.y < camera_offset_move_area.x:
                self.__dest_camera_offset.y += CAMERA_OFFSET_SPEED

            self.__dest_camera_offset.x = max(
                self.__dest_camera_offset.x, -(self.__map_size[0] * TILE_SIZE - draw_screen_size.x / zoom))
            self.__dest_camera_offset.y = max(
                self.__dest_camera_offset.y, -(self.__map_size[1] * TILE_SIZE - draw_screen_size.y / zoom))
            self.__dest_camera_offset.x = min(self.__dest_camera_offset.x, 0)
            self.__dest_camera_offset.y = min(self.__dest_camera_offset.y, 0)

        self.__real_camera_offset += (self.__dest_camera_offset - self.__real_camera_offset) \
                                        / CAMERA_SMOOTH * dt 
        self.__camera_offset = Vector2(
            int(self.__real_camera_offset.x), int(self.__real_camera_offset.y)) 
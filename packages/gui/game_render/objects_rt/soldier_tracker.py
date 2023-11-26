from pygame import Vector2

from packages.gui.game_render.objects_rt.object_rt import ObjectRT
from ....game_logic.objects.soldiers import Soldier
from ...const import TILE_SIZE
from ..particle import BloodParticle, ParticleController
from .soldier_rt import SoldierRT
from .object_tracker import ObjectTracker

class SoldierTracker(ObjectTracker):
    def __init__(self, path: list[tuple[int, int]], particle_controller: ParticleController):
        super().__init__(particle_controller)
        SoldierRT.path = path
    
    def get_new_object(self, logic_object: Soldier, side: str) -> ObjectRT:
        return SoldierRT(
            logic_object.id,
            logic_object.position,
            logic_object.name,
            side,
            logic_object.__dict__()
        )

    def update(self, logic_soldiers: dict[str, dict[Soldier]], dt: float, mouse_pos: Vector2, game_speed: float) -> None:
        
        super().update(logic_soldiers, dt, mouse_pos, game_speed)

        first = {
            side: None if not logic_soldiers[side] 
            else self.objects_rt[side][logic_soldiers[side][0].id]
            for side in ('left', 'right')
        } 

        if first['left'] is not None and first['right'] is not None:
            distance = abs(first['left']['position'] - first['right']['position'])
            for side in ('left', 'right'):
                first[side].set_state('fight' if distance <= 1 else 'walk')
                
        else:
            for side in ('left', 'right'):
                if first[side] is not None:
                    first[side].set_state('walk')

        for side in ('left', 'right'):
            for i in range(1, len(logic_soldiers[side])):
                rt_soldier = self.objects_rt[side][logic_soldiers[side][i].id]
                pre_rt_soldier = self.objects_rt[side][logic_soldiers[side][i - 1].id]
                distance = abs(rt_soldier['position'] - pre_rt_soldier['position'])
                if distance == 0 or (distance == 1 and pre_rt_soldier.state != 'walk'):
                    if abs(rt_soldier['position'] - first['left' if side == 'right' else 'right']['position']) <= rt_soldier['range']:
                        state = 'fight'
                    else:
                        state = 'idle'
                else:
                    state = 'walk'
                rt_soldier.set_state(state)

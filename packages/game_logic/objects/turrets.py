from .soldiers import Soldiers

class _Turret():
    def __init__(self, cords, id) -> None:
        self.cords = cords
        self.attack = 10
        self.id = id
        
    def _shoot(self, soldiers: Soldiers) -> None:
        for soldier in soldiers.soldiers:
            if soldier.position == self.cords:
                soldier.hp -= self.attack
                break

    def get_cords(self) -> tuple[int, int]:
        return self.cords
    def get_id(self) -> int:
        return self.id

    

class Turrets():
    def __init__(self) -> None:
        self.turrets = []
        self.next_id = 0

    def spawn(self, cords: tuple[int, int]) -> None:
        self.turrets.append(_Turret(cords), id=self.next_id)
        self.next_id += 1

    def shoot(self, soldiers: Soldiers) -> None:
        soldiers._sort_soldiers(reverse=True) if soldiers.side == 'left' else soldiers._sort_soldiers()

        for turret in self.turrets:
            turret._shoot(soldiers)

        soldiers._clean_dead()
        
    

        
                    

        
        

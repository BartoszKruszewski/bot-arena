class _Soldier():
    def __init__(self, id, position) -> None:
        self.id = id
        self.hp = 100
        self.damage = 10

        self.can_move = True
        self.position = position

    def _fight(self, enemy: '_Soldier') -> None:
        enemy.hp -= self.damage
        self.hp -= enemy.damage

    def get_id(self) -> int:
        return self.id
    
    def get_hp(self) -> int:
        return self.hp
    
    def get_position(self) -> int:
        return self.position

class Soldiers():
    def __init__(self, side, path) -> None:
        self.side = side
        self.soldiers = []
        self.next_id = 0
        self.path = path

    def _position_to_cords(self, position: int) -> tuple[int, int]:
        return self.path[position]

    def _sort_soldiers(self, reverse=False) -> None:  
        self.soldiers.sort(key=lambda soldier: soldier.position, reverse=reverse)

    def _clean_dead(self) -> None:
        self.soldiers = [soldier for soldier in self.soldiers if soldier.hp > 0]

    def can_spawn(self) -> bool:
        return all(soldier.position != 0 for soldier in self.soldiers)
        
    def fight(self, right_soldiers: 'Soldiers') -> None:
        if self.side == "right": Exception("You can't fight from right side")

        if not self.soldiers or not right_soldiers.soldiers:
            return

        self._sort_soldiers()
        right_soldiers._sort_soldiers()

        if self.soldiers[-1].position == right_soldiers.soldiers[0].position or \
           self.soldiers[-1].position + 1 == right_soldiers.soldiers[0].position:
            self.soldiers[-1]._fight(right_soldiers.soldiers[0])
            self.soldiers[-1].can_move = False
            right_soldiers.soldiers[0].can_move = False

        self._clean_dead()
        right_soldiers._clean_dead()

    def is_win(self) -> bool:
        if self.side == 'left':
            return self.soldiers and self.soldiers[-1].position == len(self.path)
        else:
            return self.soldiers and self.soldiers[0].position == -1

    def move(self) -> None:
        for soldier in self.soldiers:
            if soldier.can_move:
                soldier.position += 1 if self.side == 'left' else -1

        for soldier in self.soldiers:
            soldier.can_move = True

    def spawn(self) -> None:
        if self.can_spawn():
            self.soldiers.append(_Soldier(self.next_id, 0 if self.side == 'left' else len(self.path) - 1))
            self.next_id += 1

    def __iter__(self):
        for soldier in self.soldiers:
            yield self.path[soldier.position]

    
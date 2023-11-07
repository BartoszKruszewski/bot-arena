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

class Soldiers():
    def __init__(self, side, path) -> None:
        self.side = side
        self.soldiers = []
        self.next_id = 0
        self.path = path

    def _position_to_cords(self, position: int) -> tuple[int, int]:
        return self.path[position]

    def _sort_soldiers(self) -> None:
        """Sorts soldiers by position, where 0 is the closest to the ENEMY base.
        """

        self.soldiers.sort(key=lambda soldier: soldier.position, 
                           reverse=True if self.side == 'left' else False)

    def _clean_dead(self) -> None:
        self.soldiers = list(filter(lambda soldier: soldier.hp > 0, self.soldiers))

    def can_spawn(self) -> bool:
        MY_BASE = 0 if self.side == 'left' else len(self.path) - 1
        return all(soldier.position != MY_BASE for soldier in self.soldiers)
        
    def fight(self, right_soldiers: 'Soldiers') -> None:
        if self.side == "right": Exception("You can't fight from right side")

        for soldier in self.soldiers:
            soldier.can_move = True

        for soldier in right_soldiers.soldiers:
            soldier.can_move = True

        if not self.soldiers or not right_soldiers.soldiers:
            return

        self._sort_soldiers()
        right_soldiers._sort_soldiers()

        last_soldier = self.soldiers[0]
        first_enemy_soldier = right_soldiers.soldiers[0]

        if last_soldier.position == first_enemy_soldier.position or \
            last_soldier.position + 1 == first_enemy_soldier.position:
            last_soldier._fight(first_enemy_soldier)
            last_soldier.can_move = False
            first_enemy_soldier.can_move = False

    def is_win(self) -> bool:
        ENEMY_BASE = len(self.path) if self.side == 'left' else -1

        return any(soldier.position == ENEMY_BASE for soldier in self.soldiers)

    def move(self) -> None:
        FORWARD = 1
        BACKWARD = -1

        self._sort_soldiers()

        for soldier in self.soldiers:
            if not soldier.can_move:
                continue

            new_position = soldier.position + (FORWARD if self.side == 'left' else BACKWARD)
            
            my_positions = [soldier.position for soldier in self.soldiers]

            if new_position in my_positions:
                soldier.can_move = False
                continue

            soldier.position = new_position

        self._clean_dead()

    def spawn(self) -> None:
        if self.can_spawn():
            self.soldiers.append(_Soldier(self.next_id, 0 if self.side == 'left' else len(self.path) - 1))
            self.next_id += 1

    def __iter__(self):
        for soldier in self.soldiers:
            yield self.path[soldier.position]

    
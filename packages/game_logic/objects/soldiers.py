class Soldier():
    def __init__(self, id, position) -> None:
        self.id = id
        self.max_hp = 100
        
        self.hp = 100
        self.damage = 10

        self.did_move = False
        self.position = position

class Soldiers():
    def __init__(self, side, path) -> None:
        self.side = side
        self.soldiers = []
        self.next_id = 0
        self.path = path

        self.is_win = False

    def __sort_soldiers(self) -> None:
        """Sorts soldiers by position, where 0 is the closest to the ENEMY base.
        """

        self.soldiers.sort(key=lambda soldier: soldier.position, 
                           reverse=True if self.side == 'left' else False)

    def __fight_soldiers(self, soldier1: Soldier, soldier2: Soldier) -> None:
        soldier1.hp -= soldier2.damage
        soldier2.hp -= soldier1.damage

    def clear_dead(self) -> None:
        self.soldiers = list(filter(lambda soldier: soldier.hp > 0, self.soldiers))
        
        ENEMY_BASE = -1 if self.side == 'right' else len(self.path)
        if any(soldier.position == ENEMY_BASE for soldier in self.soldiers):
            self.is_win = True
        self.soldiers = list(filter(lambda soldier: soldier.position != ENEMY_BASE, self.soldiers))

        self.__sort_soldiers()

    def can_spawn(self) -> bool:
        MY_BASE = 0 if self.side == 'left' else len(self.path) - 1
        return all(soldier.position != MY_BASE for soldier in self.soldiers)
        
    def fight(self, right_soldiers: 'Soldiers') -> None:
        if self.side == "right": Exception("You can't fight from right side")

        for soldier in self.soldiers:
            soldier.did_move = False

        for soldier in right_soldiers.soldiers:
            soldier.did_move = False

        if not self.soldiers or not right_soldiers.soldiers:
            return

        last_soldier = self.soldiers[0]
        first_enemy_soldier = right_soldiers.soldiers[0]

        if last_soldier.position == first_enemy_soldier.position or \
            last_soldier.position + 1 == first_enemy_soldier.position:
            self.__fight_soldiers(last_soldier, first_enemy_soldier)
            last_soldier.did_move = True
            first_enemy_soldier.did_move = True

    def move(self) -> None:
        FORWARD = 1
        BACKWARD = -1

        for soldier in self.soldiers:
            if soldier.did_move:
                continue

            new_position = soldier.position + (FORWARD if self.side == 'left' else BACKWARD)
            
            my_positions = [soldier.position for soldier in self.soldiers]

            if new_position in my_positions:
                soldier.did_move = True
                continue

            soldier.position = new_position
            

    def spawn(self) -> None:
        if self.can_spawn():
            self.soldiers.append(Soldier(self.next_id, 0 if self.side == 'left' else len(self.path) - 1))
            self.next_id += 1

    def __iter__(self):
        for soldier in self.soldiers:
            yield self.path[soldier.position]

    
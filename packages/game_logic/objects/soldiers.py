from packages.game_logic.stats import SOLDIERS_STATS

class Soldier():
    def __init__(self, id, position, stats, name) -> None:
        self.id = id
        self.max_hp = stats['max_hp']
        self.damage = stats['damage']
        self.range = stats['range']
        self.name = name

        self.hp = self.max_hp
        self.did_move = False
        self.position = position

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "range": self.range,
            "name": self.name,
            "hp": self.hp,
            "position": self.position
        }
    
    def copy(self):
        return Soldier(self.id, self.position, SOLDIERS_STATS[self.name], self.name)

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

    def __attack_soldier(self, soldier: Soldier, enemy_soldier: Soldier) -> None:
        soldier.did_move = True
        enemy_soldier.hp -= soldier.damage
        # print(f"Side {self.side} Soldier {soldier.position} attacked soldier {enemy_soldier.position} for {soldier.damage} damage")

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
        
    def fight(self, enemy_soldiers: 'Soldiers') -> None:
        for soldier in self.soldiers:
            soldier.did_move = False

        if len(self.soldiers) == 0 or len(enemy_soldiers.soldiers) == 0:
            return

        def distance(soldier: Soldier, enemy_soldier: Soldier) -> int:
            return abs(soldier.position - enemy_soldier.position)

        def is_near(soldier: Soldier, enemy_soldier: Soldier) -> bool:
            return distance(soldier, enemy_soldier) <= 1

        def is_any_attack() -> bool:
            left_first = self.soldiers[0]
            right_first = enemy_soldiers.soldiers[0]
            if not is_near(left_first, right_first):
                return False
            self.__attack_soldier(left_first, right_first)
            return True
        
        if not is_any_attack():
            return
        
        def can_soldier_shoot(index: int) -> bool:
            for i in range(index, 0, -1):
                if not is_near(self.soldiers[i], self.soldiers[i-1]):
                    return False
                if self.soldiers[i-1].did_move:
                    return True
            raise Exception('This should not happen')
                    
        for i, soldier in enumerate(self.soldiers[1:], 1):
            if can_soldier_shoot(i) and distance(soldier, enemy_soldiers.soldiers[0]) <= soldier.range:
                self.__attack_soldier(soldier, enemy_soldiers.soldiers[0])

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
            
    def spawn(self, name='swordsman') -> None:
        if self.can_spawn():
            MY_BASE = 0 if self.side == 'left' else len(self.path) - 1
            new_soldier = Soldier(self.next_id, MY_BASE, SOLDIERS_STATS[name], name)
            self.soldiers.append(new_soldier)
            self.next_id += 1

    def __iter__(self):
        for soldier in self.soldiers:
            yield self.path[soldier.position]

    def copy(self):
        soldiers_copy = Soldiers(self.side, self.path)
        soldiers_copy.soldiers = [soldier.copy() for soldier in self.soldiers]
        soldiers_copy.next_id = self.next_id
        soldiers_copy.is_win = self.is_win
        return soldiers_copy
    
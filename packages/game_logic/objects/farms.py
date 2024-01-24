class Farm():
    def __init__(self, cords, id) -> None:
        self.cords = cords
        self.id = id
    
    def __dict__(self) -> dict:
        return {
            "cords": self.cords,
            "id": self.id
        }
    
    def copy(self):
        return Farm(self.cords, self.id)
    
    def get_coordinates(self):
        return self.cords

class Farms():
    def __init__(self, path) -> None:
        self.farms = []
        self.next_id = 0
        self.path = path

    def spawn(self, cords: tuple[int, int]) -> None:
        self.farms.append(Farm(cords, id=self.next_id))
        self.next_id += 1

    def __iter__(self) -> iter:
        for turret in self.farms:
            yield turret.cords

    def __len__(self) -> int:
        return len(self.farms)
        
    def copy(self):
        farms_copy = Farms(self.path)
        farms_copy.farms = [farm.copy() for farm in self.farms]
        farms_copy.next_id = self.next_id
        return farms_copy
class Obstacle:
    def __init__(self, cords, id) -> None:
        self.cords = cords
        self.id = id
    
    def __dict__(self) -> dict:
        return {
            "cords": self.cords,
            "id": self.id
        }

class Obstacles():
    def __init__(self) -> None:
        self.obstacles = []
        self.next_id = 0

    def spawn(self, cords: tuple[int, int]) -> None:
        self.obstacles.append(Obstacle(cords, id=self.next_id))
        self.next_id += 1

    def __iter__(self) -> iter:
        for obstacle in self.obstacles:
            yield obstacle.cords

    def __len__(self) -> int:
        return len(self.obstacles)
        